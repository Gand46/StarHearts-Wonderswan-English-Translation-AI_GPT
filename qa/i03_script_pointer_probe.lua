local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_path = assert(os.getenv("MESEN_TRACE_OUT"))
local state_data = assert(io.open(state_path, "rb")):read("*a")
local loaded = false
local frame = 0
local out = assert(io.open(out_path, "w"))

emu.addMemoryCallback(function()
  if not loaded then loaded = true; emu.loadSavestate(state_data) end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address, value)
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.address < 0x191E90 or converted.address > 0x191ECF then return end
  local s = emu.getState()
  out:write(string.format(
    "TEXTREAD|frame=%d|phys=%06X|cpu=%05X|value=%02X|pc=%04X:%04X|ds=%04X|si=%04X|bx=%04X|di=%04X|sp=%04X|bank2=%02X|portc2=%02X\n",
    frame, converted.address, cpu_address, value,
    s["cpu.cs"] or 0, s["cpu.ip"] or 0, s["cpu.ds"] or 0,
    s["cpu.si"] or 0, s["cpu.bx"] or 0, s["cpu.di"] or 0,
    s["cpu.sp"] or 0, s["cart.selectedBanks2"] or 0,
    emu.read(0xC2, emu.memType.wsPort, false)))
  out:flush()
end, emu.callbackType.read, 0x20000, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addEventCallback(function()
  local input = {}
  if frame >= 40 and frame < 120 then input.right = true end
  if frame >= 150 and frame < 230 and frame % 30 < 5 then input.a = true end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == 181 then
    for address = 0, 0xFFFE do
      local word = emu.read16(address, emu.memType.wsWorkRam, false)
      if word == 0x1EB0 or word == 0x1EB6 or word == 0x1ECE then
        out:write(string.format("WRAMPTR|address=%04X|value=%04X\n", address, word))
      end
    end
  end
  if frame == 260 then out:close(); emu.stop(0) end
end, emu.eventType.endFrame)
