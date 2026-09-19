local core_config = {}
for key, value in pairs(cartridge.config) do
    if key ~= "scope_python" then core_config[key] = value end
end
-- The helper program (src/service.ts) speaks lines of JSON (src/wire.ts): a
-- call is answered by id; what it asks or emits on its own the node serves
-- itself. A command may run for `timeout_seconds`; the call waits a little longer.
local config = cartridge.config or {}
local app = cartridge.spawn({ "bun", cartridge.root .. "/src/service.ts" },
	{ timeout_ms = ((config.timeout_seconds or 600) + 30) * 1000 })

local function call(name, args)
	local reply = app:request({ call = name, args = args })
	if reply.error ~= nil then error(reply.error, 0) end
	return reply.result
end

call("apply", core_config)
for _, name in ipairs({ "prd", "tool.prd", "source.board", "asp.prd" }) do
	cartridge.listen(name, function(args) return call(name, args) end)
end
cartridge.on_dispose(function() pcall(call, "dispose"); app:kill() end)

local scope_detail
for _, name in ipairs({ "scope.detail.plan", "scope.detail.task" }) do
    cartridge.listen(name, function(args)
        if scope_detail == nil then
            scope_detail = cartridge.spawn({ cartridge.config.scope_python, cartridge.root .. "/src/scope_detail.py" }, { timeout_ms = 1500 })
        end
        local reply = scope_detail:request({ args = args })
        if reply.error ~= nil then error(reply.error, 0) end
        return reply.result
    end)
end
cartridge.on_dispose(function() if scope_detail ~= nil then scope_detail:kill() end end)
