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

call("apply", cartridge.config)
for _, name in ipairs({ "prd", "tool.prd", "source.board", "graph.announce" }) do
	cartridge.listen(name, function(args) return call(name, args) end)
end
cartridge.on_dispose(function() pcall(call, "dispose"); app:kill() end)
