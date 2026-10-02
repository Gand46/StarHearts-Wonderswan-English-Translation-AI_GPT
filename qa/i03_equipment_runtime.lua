local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_dir = assert(os.getenv("MESEN_OUTDIR"))
local report_path = assert(os.getenv("MESEN_TRACE_OUT"))
local state_data = assert(io.open(state_path, "rb")):read("*a")
local loaded = false
local frame = 0
local hits = {wpn = 0, arm = 0}
local first_capture = false

local ranges = {
  {id = "wpn", first = 0x2192F6, last = 0x2192F8},
  {id = "arm", first = 0x2192FE, last = 0x219300},
}
local by_address = {}
for _, range in ipairs(ranges) do
  for address = range.first, range.last do by_address[address] = range.id end
end

local function screenshot(name)
  local f = assert(io.open(out_dir .. "/" .. name .. ".png", "wb"))
  f:write(emu.takeScreenshot())
  f:close()
end

emu.addMemoryCallback(function()
  if not loaded then
    loaded = true
    emu.loadSavestate(state_data)
  end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address)
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  local id = by_address[converted.address]
  if not id then return end
  hits[id] = hits[id] + 1
  if not first_capture then first_capture = true end
end, emu.callbackType.read, 0x20000, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

local function pulse(first, width)
  return frame >= first and frame < first + (width or 5)
end

emu.addEventCallback(function()
  local input = {}
  input.down2 = pulse(40)
  input.down = pulse(140)
  input.a = pulse(240) or pulse(380) or pulse(500)
  input.b = pulse(620) or pulse(740)
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == 100 then screenshot("equipment_open_f20") end
  if first_capture and frame > 45 and frame < 850 then
    screenshot("equipment_bank21_first_read_f20")
    first_capture = false
  end
  if frame == 850 then
    screenshot("equipment_route_end_f20")
    local out = assert(io.open(report_path, "w"))
    out:write(string.format(
      '{"checkpoint":"F19_room98_NAV_ONLY","route":"Y3/down2 equipment","frames":850,"wpn_hits":%d,"arm_hits":%d}\n',
      hits.wpn, hits.arm))
    out:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
