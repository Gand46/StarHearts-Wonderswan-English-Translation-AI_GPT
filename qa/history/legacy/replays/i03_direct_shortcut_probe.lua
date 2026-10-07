local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_dir = assert(os.getenv("MESEN_OUTDIR"))
local button = assert(os.getenv("MESEN_BUTTON"))
local state_data = assert(io.open(state_path, "rb")):read("*a")
local frame = 0
local loaded = false
local hits = {wpn = 0, arm = 0, buy = 0, sell = 0}
local targets = {
  wpn = {0x2192F6, 0x2192F8}, arm = {0x2192FE, 0x219300},
  buy = {0x219432, 0x219434}, sell = {0x21943A, 0x21943D},
}
local by_address = {}
for id, range in pairs(targets) do
  for address = range[1], range[2] do by_address[address] = id end
end

local function screenshot(suffix)
  local f = assert(io.open(out_dir .. "/direct_" .. button .. "_" .. suffix .. ".png", "wb"))
  f:write(emu.takeScreenshot())
  f:close()
end

emu.addMemoryCallback(function()
  if not loaded then loaded = true; emu.loadSavestate(state_data) end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address)
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  local id = by_address[converted.address]
  if id then hits[id] = hits[id] + 1 end
end, emu.callbackType.read, 0x20000, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

local function pulse(first, width) return frame >= first and frame < first + (width or 5) end
emu.addEventCallback(function()
  local input = {}
  if pulse(40) then input[button] = true end
  input.down = pulse(140) or pulse(340)
  input.right = pulse(180) or pulse(380)
  input.a = pulse(220) or pulse(420) or pulse(540)
  input.b = pulse(660)
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == 100 then screenshot("open") end
  if frame == 300 then screenshot("selected") end
  if frame == 600 then screenshot("deep") end
  if frame == 760 then
    screenshot("end")
    local f = assert(io.open(out_dir .. "/direct_" .. button .. "_trace.json", "w"))
    f:write(string.format(
      '{"button":"%s","wpn_hits":%d,"arm_hits":%d,"buy_hits":%d,"sell_hits":%d}\n',
      button, hits.wpn, hits.arm, hits.buy, hits.sell))
    f:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
