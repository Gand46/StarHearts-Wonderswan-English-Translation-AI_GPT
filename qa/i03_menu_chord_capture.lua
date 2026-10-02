local state_path = assert(os.getenv("MESEN_BASESTATE"))
local capture_path = assert(os.getenv("MESEN_CAPTURE_PATH"))
local report_path = assert(os.getenv("MESEN_LUA_REPORT"))
local direction = assert(os.getenv("MESEN_MENU_DIRECTION"))
local state = assert(io.open(state_path, "rb")):read("*a")
local frame = 0
local loaded = false

emu.addMemoryCallback(function()
  if not loaded then loaded = true; emu.loadSavestate(state) end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addEventCallback(function()
  local input = {}
  if frame >= 30 and frame < 82 then input.start = true end
  if frame >= 72 and frame < 78 then input[direction] = true end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == 150 then
    local image = assert(io.open(capture_path, "wb")); image:write(emu.takeScreenshot()); image:close()
    local report = assert(io.open(report_path, "w")); report:write(string.format('{"checkpoint":"F19_room98_NAV_ONLY","chord":"START+%s","frame":150}\n', direction)); report:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
