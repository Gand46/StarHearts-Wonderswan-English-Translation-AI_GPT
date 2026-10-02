local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_dir = assert(os.getenv("MESEN_OUTDIR"))
local report_path = assert(os.getenv("MESEN_TRACE_OUT"))
local target = tonumber(os.getenv("MESEN_TARGET_OFFSET") or "7C20", 16)
local state_data = assert(io.open(state_path, "rb")):read("*a")
local frame = 0
local loaded, injected = false, false
local hits = 0
local out = assert(io.open(report_path, "w"))

emu.addMemoryCallback(function()
  if not loaded then loaded = true; emu.loadSavestate(state_data) end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if injected then return end
  local s = emu.getState()
  if frame >= 140 and frame <= 160 then
    out:write(string.format("HOOK|frame=%d|si=%04X|ip=%04X\n", frame,
      s["cpu.si"] or 0, s["cpu.ip"] or 0)); out:flush()
  end
  if (s["cpu.si"] or 0) == 0x1EAE then
    s["cpu.si"] = target
    s["cpu.es"] = 0x2000
    s["cart.selectedBanks2"] = 0xE1
    emu.setState(s)
    emu.write(0xC2, 0xE1, emu.memType.wsPort)
    emu.write(0xCACA, 0xE1, emu.memType.wsWorkRam)
    emu.write16(0xCACD, target, emu.memType.wsWorkRam)
    emu.write16(0xCACF, 0x2000, emu.memType.wsWorkRam)
    injected = true
    out:write(string.format("INJECT|frame=%d|port_c2=%02X|si=%04X\n",
      frame, emu.read(0xC2, emu.memType.wsPort, false), target)); out:flush()
  end
end, emu.callbackType.exec, 0x93151, 0x93151, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address, value)
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  if converted.address >= 0x210000 and converted.address <= 0x21FFFF then
    hits = hits + 1
    if hits <= 1024 then
      local s = emu.getState()
      out:write(string.format("READ|frame=%d|phys=%06X|value=%02X|pc=%04X:%04X\n",
        frame, converted.address, value, s["cpu.cs"] or 0, s["cpu.ip"] or 0))
    end
  end
end, emu.callbackType.read, 0x20000, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addEventCallback(function()
  local input = {}
  if frame >= 40 and frame < 120 then input.right = true end
  if frame >= 150 and frame < 360 and frame % 30 < 5 then input.a = true end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame >= 150 and frame <= 420 and frame % 30 == 0 then
    local image = assert(io.open(string.format("%s/speaker_activation_%04X_f%03d.png", out_dir, target, frame), "wb"))
    image:write(emu.takeScreenshot()); image:close()
  end
  if frame == 450 then
    out:write(string.format("SUMMARY|injected=%s|bank21_hits=%d\n", tostring(injected), hits))
    out:close(); emu.stop(0)
  end
end, emu.eventType.endFrame)
