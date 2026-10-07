local state_path = assert(os.getenv("MESEN_BASESTATE"))
local capture_path = assert(os.getenv("MESEN_CAPTURE_PATH"))
local report_path = assert(os.getenv("MESEN_LUA_REPORT"))
local steps = tonumber(os.getenv("MESEN_MENU_STEPS") or "0")
local state = assert(io.open(state_path, "rb")):read("*a")
local frame = 0
local loaded = false

emu.addMemoryCallback(function()
  if not loaded then loaded = true; emu.loadSavestate(state) end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addEventCallback(function()
  local input = {}
  if frame >= 30 and frame < 34 then input.start = true end
  for index = 0, steps - 1 do
    local pulse = 70 + index * 20
    if frame >= pulse and frame < pulse + 3 then input.down2 = true end
  end
  local confirm = 90 + steps * 20
  if frame >= confirm and frame < confirm + 3 then input.b = true end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  local capture_frame = 150 + steps * 20
  if frame == capture_frame then
    local image = assert(io.open(capture_path, "wb")); image:write(emu.takeScreenshot()); image:close()
    local report = assert(io.open(report_path, "w")); report:write(string.format('{"checkpoint":"F19_room98_NAV_ONLY","menu_down_steps":%d,"frame":%d}\n', steps, capture_frame)); report:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
