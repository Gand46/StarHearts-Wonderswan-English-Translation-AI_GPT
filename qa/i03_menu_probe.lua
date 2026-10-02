local state_path = assert(os.getenv("MESEN_BASESTATE"))
local output_dir = assert(os.getenv("MESEN_OUTDIR"))
local report_path = assert(os.getenv("MESEN_LUA_REPORT"))
local state = assert(io.open(state_path, "rb")):read("*a")
local frame = 0
local loaded = false

local function load_state()
  if not loaded then
    loaded = true
    emu.loadSavestate(state)
  end
end

local function screenshot(name)
  local file = assert(io.open(output_dir .. "/" .. name .. ".png", "wb"))
  file:write(emu.takeScreenshot())
  file:close()
end

emu.addMemoryCallback(load_state, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addEventCallback(function()
  local input = {}
  if frame >= 20 and frame < 24 then input.start = true end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == 10 then screenshot("before_start") end
  if frame == 45 then screenshot("after_start_45") end
  if frame == 90 then screenshot("after_start_90") end
  if frame == 140 then
    screenshot("after_start_140")
    local report = assert(io.open(report_path, "w"))
    report:write("loaded natural NAV_ONLY checkpoint; pressed START; captured frames 10,45,90,140\n")
    report:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
