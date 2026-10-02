local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_dir = assert(os.getenv("MESEN_OUTDIR"))
local report_path = assert(os.getenv("MESEN_TRACE_OUT"))
local module_index = assert(tonumber(os.getenv("MESEN_MODULE_INDEX")))
local force_offset = tonumber(os.getenv("MESEN_FORCE_EBC2") or "", 16)
local force_function = tonumber(os.getenv("MESEN_FORCE_FUNCTION") or "", 16)
local max_frames = tonumber(os.getenv("MESEN_MAX_FRAMES") or "1020")
local seed_entity = os.getenv("MESEN_SEED_ENTITY") == "1"
local state_data = assert(io.open(state_path, "rb")):read("*a")

local frame = 0
local loaded = false
local injected = false
local loader_entered = false
local pointer_forced = false
local opcode_entered = false
local post_inject_logged = false
local pc_trace_count = 0
local hits = 0
local unique = {}
local out = assert(io.open(report_path, "w"))

local function screenshot(tag)
  local f = assert(io.open(string.format("%s/module_%02d_%s.png", out_dir, module_index, tag), "wb"))
  f:write(emu.takeScreenshot())
  f:close()
end

emu.addMemoryCallback(function()
  if not loaded then
    loaded = true
    emu.loadSavestate(state_data)
  end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

-- Feed opcode 0x14 plus a module index to the game's main script interpreter.
-- Its native handler at 9000:338C invokes the real Bank 21 loader at 9000:BD30.
emu.addMemoryCallback(function()
  if injected or frame < 120 then return end
  local s = emu.getState()
  emu.write16(0x0100, 0x0014, emu.memType.wsMemory)
  emu.write16(0x0102, module_index, emu.memType.wsMemory)
  emu.write16(0x0104, 0x0000, emu.memType.wsMemory)
  emu.write16(0xCACD, 0x0100, emu.memType.wsWorkRam)
  emu.write16(0xCACF, 0x0000, emu.memType.wsWorkRam)
  injected = true
  out:write(string.format(
    "INJECT|frame=%d|opcode=%04X|index=%d|stream=0000:0100|pc=%04X:%04X\n",
    frame, emu.read16(0x0100, emu.memType.wsMemory), module_index,
    s["cpu.cs"] or 0, s["cpu.ip"] or 0))
  out:flush()
end, emu.callbackType.exec, 0x93148, 0x93148, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if not injected or post_inject_logged then return end
  post_inject_logged = true
  local s = emu.getState()
  local linear = ((((s["cpu.es"] or 0) << 4) + (s["cpu.si"] or 0)) & 0xFFFFF)
  out:write(string.format(
    "STREAM_READ|frame=%d|es=%04X|si=%04X|linear=%05X|word=%04X\n",
    frame, s["cpu.es"] or 0, s["cpu.si"] or 0, linear,
    emu.read16(linear, emu.memType.wsMemory)))
  out:flush()
end, emu.callbackType.exec, 0x93151, 0x93151, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if not injected or pc_trace_count >= 80 then return end
  pc_trace_count = pc_trace_count + 1
  local s = emu.getState()
  out:write(string.format("PC|%02d|%04X:%04X|bx=%04X|si=%04X\n",
    pc_trace_count, s["cpu.cs"] or 0, s["cpu.ip"] or 0,
    s["cpu.bx"] or 0, s["cpu.si"] or 0))
  out:flush()
end, emu.callbackType.exec, 0x93140, 0x93420, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if opcode_entered then return end
  opcode_entered = true
  local s = emu.getState()
  out:write(string.format(
    "OPCODE28|frame=%d|cs=%04X|ip=%04X|ax=%04X|es=%04X|si=%04X\n",
    frame, s["cpu.cs"] or 0, s["cpu.ip"] or 0, s["cpu.ax"] or 0,
    s["cpu.es"] or 0, s["cpu.si"] or 0))
  out:flush()
end, emu.callbackType.exec, 0x9338C, 0x9338C, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if loader_entered then return end
  loader_entered = true
  local s = emu.getState()
  out:write(string.format(
    "LOADER|frame=%d|cs=%04X|ip=%04X|ax=%04X|sp=%04X\n",
    frame, s["cpu.cs"] or 0, s["cpu.ip"] or 0, s["cpu.ax"] or 0, s["cpu.sp"] or 0))
  out:flush()
end, emu.callbackType.exec, 0x9BD30, 0x9BD30, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if (not force_offset and not force_function) or pointer_forced or not loader_entered then return end
  local target_offset = force_offset
  local target_segment = 0x2000
  if force_function then
    target_offset = 0x0200
    target_segment = 0x0000
    emu.write16(target_offset, force_function, emu.memType.wsMemory)
    emu.write16(target_offset + 2, 0xC10E, emu.memType.wsMemory)
  end
  emu.write16(0xEBC2, target_offset, emu.memType.wsWorkRam)
  emu.write16(0xEBC4, target_segment, emu.memType.wsWorkRam)
  if seed_entity then
    emu.write16(0xD24B, 0x0001, emu.memType.wsWorkRam)
    emu.write16(0xD24D, 0x0600, emu.memType.wsWorkRam)
    emu.write16(0xD24F, 0x0305, emu.memType.wsWorkRam)
  end
  pointer_forced = true
  out:write(string.format("FORCE_EBC2|frame=%d|offset=%04X|segment=%04X|function=%s|seed_entity=%s\n",
    frame, target_offset, target_segment,
    force_function and string.format("%04X", force_function) or "none", tostring(seed_entity)))
  out:flush()
end, emu.callbackType.exec, 0x9BE71, 0x9BE71, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address, value)
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  local address = converted.address
  if address < 0x210000 or address > 0x21FFFF then return end
  hits = hits + 1
  unique[address] = (unique[address] or 0) + 1
  if hits <= 512 then
    local s = emu.getState()
    out:write(string.format(
      "READ|frame=%d|phys=%06X|value=%02X|pc=%04X:%04X\n",
      frame, address, value, s["cpu.cs"] or 0, s["cpu.ip"] or 0))
  end
end, emu.callbackType.read, 0x20000, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

local function pulse(first, width)
  return frame >= first and frame < first + (width or 5)
end

emu.addEventCallback(function()
  local input = {}
  if frame >= 40 and frame < 120 then input.right = true end
  input.a = pulse(160) or pulse(520) or pulse(720) or pulse(900)
  if frame >= 1100 and frame % 200 < 5 then input.a = true end
  input.down = pulse(620)
  input.right = pulse(820)
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == 90 or frame == 150 or frame == 240 or frame == 360 or
      frame == 500 or frame == 600 or frame == 700 or frame == 800 or frame == 900 or
      (frame >= 960 and frame <= 1010 and frame % 2 == 0) or
      (frame >= 1100 and frame <= 1500 and frame % 100 == 0) then
    screenshot(string.format("f%03d", frame))
  end
  if frame == max_frames then
    local unique_count = 0
    for _ in pairs(unique) do unique_count = unique_count + 1 end
    if seed_entity then
      local name_bytes = {}
      for address = 0xD2AD, 0xD2BC do
        name_bytes[#name_bytes + 1] = string.format("%02X", emu.read(address, emu.memType.wsWorkRam))
      end
      out:write("ENTITY_NAME|d24b_plus_62=" .. table.concat(name_bytes, " ") .. "\n")
    end
    out:write(string.format(
      "SUMMARY|index=%d|injected=%s|bank21_hits=%d|unique=%d\n",
      module_index, tostring(injected), hits, unique_count))
    out:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
