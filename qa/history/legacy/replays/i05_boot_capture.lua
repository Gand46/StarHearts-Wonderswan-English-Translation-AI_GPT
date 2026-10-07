local capture_path = assert(os.getenv("MESEN_CAPTURE_PATH"))
local report_path = assert(os.getenv("MESEN_LUA_REPORT"))
local frame = 0

emu.addEventCallback(function()
  frame = frame + 1
  if frame == 180 then
    local image = assert(io.open(capture_path, "wb"))
    image:write(emu.takeScreenshot())
    image:close()
    local report = assert(io.open(report_path, "w"))
    report:write('{"cold_boot":true,"frame":180,"surface":"title"}\n')
    report:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
