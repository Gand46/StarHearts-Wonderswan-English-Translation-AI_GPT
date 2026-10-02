local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_dir = assert(os.getenv("MESEN_OUTDIR"))
local report_path = assert(os.getenv("MESEN_TRACE_OUT"))
local state_data = assert(io.open(state_path, "rb")):read("*a")
local loaded, captured = false, false
local frame = 0
local hits = {wpn = 0, arm = 0}
local by_address = {}
for address = 0x2192F6, 0x2192F8 do by_address[address] = "wpn" end
for address = 0x2192FE, 0x219300 do by_address[address] = "arm" end

local function screenshot(name)
  local f = assert(io.open(out_dir .. "/" .. name .. ".png", "wb"))
  f:write(emu.takeScreenshot()); f:close()
end

emu.addMemoryCallback(function()
  if not loaded then loaded = true; emu.loadSavestate(state_data) end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address)
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  local id = by_address[converted.address]
  if id then hits[id] = hits[id] + 1; captured = true end
end, emu.callbackType.read, 0x20000, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

local down_pulses = {180, 220, 260}
local function pulse(first) return frame >= first and frame < first + 5 end
local function any_pulse(values)
  for _, value in ipairs(values) do if pulse(value) then return true end end
  return false
end

emu.addEventCallback(function()
  local input = {}
  input.down2 = pulse(40)
  input.right = pulse(140)
  input.down = any_pulse(down_pulses)
  input.a = pulse(360)
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == 340 then screenshot("status_selected_f20") end
  if frame == 460 then screenshot("status_open_f20") end
  if captured and frame > 360 and frame < 600 then screenshot("status_bank21_read_f20") end
  captured = false
  if frame == 600 then
    local f = assert(io.open(report_path, "w"))
    f:write(string.format(
      '{"checkpoint":"F19_room98_NAV_ONLY","route":"Y3/down2 > right > down x3 > A","wpn_hits":%d,"arm_hits":%d}\n',
      hits.wpn, hits.arm))
    f:close(); emu.stop(0)
  end
end, emu.eventType.endFrame)
