-- The helper program (src/service.ts) speaks lines of JSON (src/wire.ts). A
-- call is answered by id; while answering, the program may ask the base first
-- (`bail`, `host`), served here and answered with the next line. Lines it
-- writes on its own (events, asks between calls) come through a FIFO `cat`
-- relays, since this node runs nothing while it waits for an answer.
-- A command may run for `timeout_seconds`; the call waits a little longer.
local config = cartridge.config or {}
local app = cartridge.spawn({ "bun", cartridge.root .. "/src/service.ts" },
	{ timeout_ms = ((config.timeout_seconds or 600) + 30) * 1000 })

local function serve(line)
	local ok, result = pcall(function()
		if line.bail then return cartridge.bail(line.bail, line.args) end
		if line.host then return cartridge.host(line.host, line.params) end
		if line.event then return cartridge.emit(line.event, line.data) end
		if line.notify then return cartridge.notify(line.notify, line.data) end
		if line.publish then return cartridge.publish(line.publish, line.data) end
		error("unknown line", 0)
	end)
	if ok then return { id = line.id, result = result } end
	return { id = line.id, error = tostring(result) }
end

local function call(name, args)
	local reply = app:request({ call = name, args = args })
	while reply.ask do
		local answer = serve(reply)
		reply = app:request({ answer = reply.ask, result = answer.result, error = answer.error })
	end
	if reply.error ~= nil then error(reply.error, 0) end
	return reply.result
end

local pump = cartridge.spawn({ "/bin/cat", call("pump") })
pump:on_line(function(line)
	if type(line) ~= "table" then return end
	local answer = serve(line)
	if line.id then app:send(answer) elseif answer.error then error(answer.error, 0) end
end)
call("apply", cartridge.config)

for _, name in ipairs({ "prd", "tool.prd", "source.board", "graph.announce" }) do
	cartridge.listen(name, function(args) return call(name, args) end)
end
cartridge.on_dispose(function() pcall(call, "dispose"); app:kill(); pump:kill() end)
