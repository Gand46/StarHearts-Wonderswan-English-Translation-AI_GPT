local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_path = assert(os.getenv("MESEN_TRACE_OUT"))
local state_data = assert(io.open(state_path, "rb")):read("*a")
local out = assert(io.open(out_path, "w"))
local loaded = false
local frame = 0
local hits = 0
local logged = 0
local by_address = {}

emu.addMemoryCallback(function()
  if not loaded then loaded = true; emu.loadSavestate(state_data) end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address, value)
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  if converted.address < 0x210000 or converted.address > 0x21FFFF then return end
  hits = hits + 1
  by_address[converted.address] = (by_address[converted.address] or 0) + 1
  if logged < 4096 then
    logged = logged + 1
    local s = emu.getState()
    out:write(string.format("HIT|frame=%d|phys=%06X|cpu=%05X|value=%02X|pc=%04X:%04X\n",
      frame, converted.address, cpu_address, value, s["cpu.cs"] or 0, s["cpu.ip"] or 0))
  end
end, emu.callbackType.read, 0x20000, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addEventCallback(function()
  local input = {}
  if frame >= 40 and frame < 120 then input.right = true end
  if frame >= 150 and frame < 500 and frame % 30 < 5 then input.a = true end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == 600 then
    local unique = 0; for _ in pairs(by_address) do unique = unique + 1 end
    out:write(string.format("SUMMARY|frames=600|hits=%d|unique=%d|logged=%d\n", hits, unique, logged))
    for address, count in pairs(by_address) do
      if count > 0 then out:write(string.format("ADDRESS|phys=%06X|hits=%d\n", address, count)) end
    end
    out:close(); emu.stop(0)
  end
end, emu.eventType.endFrame)
