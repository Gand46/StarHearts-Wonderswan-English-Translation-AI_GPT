local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_path = assert(os.getenv("MESEN_TRACE_OUT"))
local capture_dir = os.getenv("MESEN_OUTDIR")
local state_data = assert(io.open(state_path, "rb")):read("*a")
local out = assert(io.open(out_path, "w"))
local loaded = false
local frame = 0
local logged = 0
local max_logged = 20000

emu.addMemoryCallback(function()
  if not loaded then loaded = true; emu.loadSavestate(state_data) end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address, value)
  if frame < 180 or frame > 240 or logged >= max_logged then return end
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  logged = logged + 1
  local s = emu.getState()
  out:write(string.format("READ|frame=%d|phys=%06X|cpu=%05X|value=%02X|pc=%04X:%04X\n",
    frame, converted.address, cpu_address, value, s["cpu.cs"] or 0, s["cpu.ip"] or 0))
end, emu.callbackType.read, 0x20000, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addEventCallback(function()
  local input = {}
  if frame >= 40 and frame < 120 then input.right = true end
  if frame >= 150 and frame < 340 and frame % 30 < 5 then input.a = true end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if capture_dir and frame >= 120 and frame <= 360 and frame % 40 == 0 then
    local image = assert(io.open(string.format("%s/neigh_frame_%03d.png", capture_dir, frame), "wb"))
    image:write(emu.takeScreenshot()); image:close()
  end
  if frame == 400 then
    out:write(string.format("SUMMARY|frames=400|logged=%d\n", logged))
    out:close(); emu.stop(0)
  end
end, emu.eventType.endFrame)
