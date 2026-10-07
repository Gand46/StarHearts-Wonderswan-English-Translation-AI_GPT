local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_path = assert(os.getenv("MESEN_TRACE_OUT"))
local route = os.getenv("MESEN_ROUTE") or "menu_sweep"
local frame_limit = tonumber(os.getenv("MESEN_FRAME_LIMIT") or "720")

local state_data = assert(io.open(state_path, "rb")):read("*a")
local out = assert(io.open(out_path, "w"))
local loaded = false
local frame = 0
local total_hits = 0

local targets = {
  {id = "speaker_indikid", first = 0x217C2A, last = 0x217C30, hits = 0},
  {id = "speaker_ricardo_1", first = 0x218286, last = 0x218289, hits = 0},
  {id = "speaker_zunter_1", first = 0x2182C6, last = 0x2182C9, hits = 0},
  {id = "speaker_ricardo_2", first = 0x218338, last = 0x21833B, hits = 0},
  {id = "speaker_zunter_2", first = 0x218568, last = 0x21856B, hits = 0},
  {id = "speaker_elder", first = 0x218CBE, last = 0x218CC1, hits = 0},
  {id = "link_error", first = 0x219610, last = 0x21962A, hits = 0},
  {id = "menu_wpn", first = 0x2192F6, last = 0x2192F8, hits = 0},
  {id = "menu_arm", first = 0x2192FE, last = 0x219300, hits = 0},
  {id = "shop_buy", first = 0x219432, last = 0x219434, hits = 0},
  {id = "shop_sell", first = 0x21943A, last = 0x21943D, hits = 0},
}

local by_address = {}
for _, target in ipairs(targets) do
  for address = target.first, target.last do by_address[address] = target end
end

emu.addMemoryCallback(function()
  if not loaded then
    loaded = true
    emu.loadSavestate(state_data)
  end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address, value)
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  local target = by_address[converted.address]
  if not target then return end
  target.hits = target.hits + 1
  total_hits = total_hits + 1
  if target.hits <= 16 then
    local s = emu.getState()
    out:write(string.format(
      "HIT|frame=%d|id=%s|phys=%06X|cpu=%05X|value=%02X|pc=%04X:%04X\n",
      frame, target.id, converted.address, cpu_address, value,
      s["cpu.cs"] or 0, s["cpu.ip"] or 0))
  end
end, emu.callbackType.read, 0x20000, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

local function pulse(first, width)
  return frame >= first and frame < first + (width or 4)
end

emu.addEventCallback(function()
  local input = {}
  if route == "menu_sweep" then
    input.start = pulse(30)
    input.up = pulse(90) or pulse(330)
    input.down = pulse(130) or pulse(370)
    input.left = pulse(170) or pulse(410)
    input.right = pulse(210) or pulse(450)
    input.a = pulse(250) or pulse(490)
    input.b = pulse(290) or pulse(530)
    input.start = input.start or pulse(310) or pulse(570)
  end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == frame_limit then
    out:write(string.format(
      "SUMMARY|frames=%d|route=%s|targets=%d|hits=%d|state_loaded=%s\n",
      frame, route, #targets, total_hits, tostring(loaded)))
    for _, target in ipairs(targets) do
      out:write(string.format(
        "TARGET|id=%s|first=%06X|last=%06X|hits=%d\n",
        target.id, target.first, target.last, target.hits))
    end
    out:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
