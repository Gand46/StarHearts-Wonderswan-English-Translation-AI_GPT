local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_dir = assert(os.getenv("MESEN_OUTDIR"))
local trace_path = assert(os.getenv("MESEN_TRACE_OUT"))
local tag = assert(os.getenv("MESEN_TAG"))
local function_ip = assert(tonumber(os.getenv("MESEN_FUNCTION_IP"), 16))
local exit_ip = assert(tonumber(os.getenv("MESEN_EXIT_IP"), 16))
local return_mode = os.getenv("MESEN_RETURN_MODE") or "intercept"
local max_frames = tonumber(os.getenv("MESEN_MAX_FRAMES") or "260")
local active_captures = os.getenv("MESEN_ACTIVE_CAPTURES") == "1"
local seed_c004 = tonumber(os.getenv("MESEN_SEED_C004") or "", 16)
local chain_ip = tonumber(os.getenv("MESEN_CHAIN_IP") or "", 16)
local state_data = assert(io.open(state_path, "rb")):read("*a")

local frame = 0
local loaded = false
local injected = false
local entered = false
local returned = false
local return_frame = nil
local hits = 0
local pc_trace_count = 0
local target_hits = {}
local out = assert(io.open(trace_path, "w"))

local targets = {}
for token in string.gmatch(os.getenv("MESEN_TARGETS") or "", "[^,]+") do
  targets[tonumber(token, 16)] = true
end

local function screenshot(suffix)
  local path = string.format("%s/%s_f21_%s.png", out_dir, tag, suffix)
  local file = assert(io.open(path, "wb"))
  file:write(emu.takeScreenshot())
  file:close()
  out:write("SCREENSHOT|" .. path .. "\n")
  out:flush()
end

emu.addMemoryCallback(function()
  if not loaded then
    loaded = true
    emu.loadSavestate(state_data)
  end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

-- Enter a real Bank 0x3A native consumer from a natural-origin checkpoint.
-- No ROM byte is changed. At the native RET, execution is parked in a
-- temporary WRAM HLT loop so the completed framebuffer remains inspectable.
emu.addMemoryCallback(function()
  if entered then return end
  entered = true
  local state = emu.getState()
  out:write(string.format(
    "ENTER|frame=%d|cs=%04X|ip=%04X|ds=%04X|es=%04X|ss=%04X|sp=%04X\n",
    frame, state["cpu.cs"] or 0, state["cpu.ip"] or 0,
    state["cpu.ds"] or 0, state["cpu.es"] or 0,
    state["cpu.ss"] or 0, state["cpu.sp"] or 0))
  out:flush()
end, emu.callbackType.exec, 0xA0000 + function_ip, 0xA0000 + function_ip,
  emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if not injected or returned or pc_trace_count >= 160 then return end
  pc_trace_count = pc_trace_count + 1
  local state = emu.getState()
  out:write(string.format(
    "PC|%03d|%04X:%04X|es=%04X|si=%04X\n",
    pc_trace_count, state["cpu.cs"] or 0, state["cpu.ip"] or 0,
    state["cpu.es"] or 0, state["cpu.si"] or 0))
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if not injected then return end
  local state = emu.getState()
  local linear = ((((state["cpu.es"] or 0) << 4) + (state["cpu.si"] or 0)) & 0xFFFFF)
  local converted = emu.convertAddress(linear, emu.memType.wsMemory, emu.cpuType.ws)
  out:write(string.format(
    "TEXT_RENDERER|frame=%d|es=%04X|si=%04X|linear=%05X|converted=%s:%s\n",
    frame, state["cpu.es"] or 0, state["cpu.si"] or 0, linear,
    converted and tostring(converted.memType) or "nil",
    converted and string.format("%06X", converted.address or 0) or "nil"))
  out:flush()
end, emu.callbackType.exec, 0x95778, 0x95778, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if not injected then return end
  local state = emu.getState()
  out:write(string.format(
    "DISPLAY_ENGINE|frame=%d|text=%04X:%04X|dest=%04X:%04X\n",
    frame, emu.read16(0xF31E, emu.memType.wsWorkRam),
    emu.read16(0xF31C, emu.memType.wsWorkRam),
    emu.read16(0xF322, emu.memType.wsWorkRam),
    emu.read16(0xF320, emu.memType.wsWorkRam)))
  out:flush()
end, emu.callbackType.exec, 0x93C00, 0x93C00, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function()
  if returned then return end
  returned = true
  return_frame = frame
  emu.write(0x0200, 0xFA, emu.memType.wsMemory)
  emu.write(0x0201, 0xF4, emu.memType.wsMemory)
  emu.write(0x0202, 0xEB, emu.memType.wsMemory)
  emu.write(0x0203, 0xFD, emu.memType.wsMemory)
  local state = emu.getState()
  if return_mode == "retf" then
    -- Let the native RETF perform the control transfer.  This flushes the
    -- V30 prefetch queue and keeps the completed panel on screen reliably.
    local sp = state["cpu.sp"] or 0
    local ss = state["cpu.ss"] or 0
    local stack_linear = (((ss << 4) + sp) & 0xFFFFF)
    emu.write16(stack_linear, 0x0200, emu.memType.wsMemory)
    emu.write16((stack_linear + 2) & 0xFFFFF, 0x0000, emu.memType.wsMemory)
    out:write(string.format(
      "RETURN_ARMED|frame=%d|mode=retf|stack=%05X|park=0000:0200\n",
      frame, stack_linear))
  else
    state["cpu.cs"] = 0x0000
    state["cpu.ip"] = 0x0200
    if state["cpu.flags"] then
      state["cpu.flags"] = state["cpu.flags"] & 0xFDFF
    end
    emu.setState(state)
    out:write(string.format("RETURN_INTERCEPT|frame=%d|park=0000:0200\n", frame))
  end
  out:flush()
end, emu.callbackType.exec, 0xA0000 + exit_ip, 0xA0000 + exit_ip,
  emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address, value)
  if not injected then return end
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  local address = converted.address
  if address < 0x370000 or address > 0x37FFFF then return end
  hits = hits + 1
  if targets[address] then target_hits[address] = (target_hits[address] or 0) + 1 end
  if hits <= 512 then
    local state = emu.getState()
    out:write(string.format(
      "READ|frame=%d|phys=%06X|value=%02X|pc=%04X:%04X|target=%s\n",
      frame, address, value, state["cpu.cs"] or 0, state["cpu.ip"] or 0,
      tostring(targets[address] == true)))
  end
end, emu.callbackType.read, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addEventCallback(function()
  frame = frame + 1
  if not injected and frame >= 120 then
    -- WRAM trampoline: pre-seed a safe return frame, then use an explicit
    -- far JMP into Bank 0x3A.  The transfer flushes the V30 prefetch queue.
    local state = emu.getState()
    local ss = state["cpu.ss"] or 0
    local sp = state["cpu.sp"] or 0
    if return_mode == "retf" then
      sp = (sp - 4) & 0xFFFF
      local stack_linear = (((ss << 4) + sp) & 0xFFFFF)
      emu.write16(stack_linear, 0x0200, emu.memType.wsMemory)
      emu.write16((stack_linear + 2) & 0xFFFFF, 0x0000, emu.memType.wsMemory)
    elseif chain_ip then
      -- Both chained routines use near RET in A000.  The first returns into
      -- chain_ip; the second returns to the native HLT byte at A974.
      sp = (sp - 4) & 0xFFFF
      local stack_linear = (((ss << 4) + sp) & 0xFFFFF)
      emu.write16(stack_linear, chain_ip, emu.memType.wsMemory)
      emu.write16((stack_linear + 2) & 0xFFFFF, 0xA974, emu.memType.wsMemory)
    else
      sp = (sp - 2) & 0xFFFF
      local stack_linear = (((ss << 4) + sp) & 0xFFFFF)
      emu.write16(stack_linear, 0xA974, emu.memType.wsMemory)
    end
    state["cpu.sp"] = sp
    if seed_c004 then
      emu.write(0xC004, seed_c004, emu.memType.wsWorkRam)
      out:write(string.format("SEED|address=C004|value=%02X\n", seed_c004))
    end
    emu.write(0x0200, 0xEA, emu.memType.wsMemory)
    emu.write16(0x0201, function_ip, emu.memType.wsMemory)
    emu.write16(0x0203, 0xA000, emu.memType.wsMemory)
    state["cpu.cs"] = 0x0000
    state["cpu.ip"] = 0x0200
    if state["cpu.flags"] then
      state["cpu.flags"] = state["cpu.flags"] & 0xFDFF
    end
    emu.setState(state)
    injected = true
    out:write(string.format(
      "INJECT|frame=%d|trampoline=0000:0200|function=A000:%04X|chain=%s|exit=A000:%04X|return_mode=%s\n",
      frame, function_ip, chain_ip and string.format("A000:%04X", chain_ip) or "none",
      exit_ip, return_mode))
    out:flush()
  end
  if return_frame then
    local delta = frame - return_frame
    if delta == 1 or delta == 10 or delta == 30 or delta == 60 then
      screenshot(string.format("d%02d", delta))
    end
  elseif active_captures and (frame == 140 or frame == 180 or frame == 220) then
    screenshot(string.format("active_f%03d", frame))
  end
  if frame == max_frames then
    for address in pairs(targets) do
      out:write(string.format("TARGET|phys=%06X|hits=%d\n", address, target_hits[address] or 0))
    end
    out:write(string.format(
      "SUMMARY|tag=%s|injected=%s|entered=%s|returned=%s|bank37_hits=%d\n",
      tag, tostring(injected), tostring(entered), tostring(returned), hits))
    out:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
