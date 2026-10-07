local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_dir = assert(os.getenv("MESEN_OUTDIR"))
local route_id = assert(os.getenv("MESEN_ROUTE"))
local state_data = assert(io.open(state_path, "rb")):read("*a")
local frame, loaded = 0, false
local hits = {owned = 0, buyprice = 0, repair = 0}
local target_by_address = {
  [0x3769D0] = "owned", [0x3769E2] = "buyprice", [0x3769F4] = "repair",
}

local routes = {
  d80_l80_u80_a = {{"down",80},{"left",80},{"up",80},{"a",30}},
  d120_l120_u80_a = {{"down",120},{"left",120},{"up",80},{"a",30}},
  d120_l160_u120_a = {{"down",120},{"left",160},{"up",120},{"a",30}},
  d160_l120_u120_a = {{"down",160},{"left",120},{"up",120},{"a",30}},
  l120_d120_l40_u120_a = {{"left",120},{"down",120},{"left",40},{"up",120},{"a",30}},
  d80_l160_d40_u140_a = {{"down",80},{"left",160},{"down",40},{"up",140},{"a",30}},
  to_tents_left40 = {{"down",120},{"left",160},{"up",120},{"left",40},{"up",90},{"a",30}},
  to_tents_right40 = {{"down",120},{"left",160},{"up",120},{"right",40},{"up",90},{"a",30}},
  to_tents_left70 = {{"down",120},{"left",160},{"up",120},{"left",70},{"up",110},{"a",30}},
  to_tents_right70 = {{"down",120},{"left",160},{"up",120},{"right",70},{"up",110},{"a",30}},
  enter_right_shop_up80 = {{"down",120},{"left",160},{"up",120},{"right",70},{"up",110},{"up",80},{"a",30}},
  enter_right_shop_up110 = {{"down",120},{"left",160},{"up",120},{"right",70},{"up",110},{"up",110},{"a",30}},
  enter_right_shop_up80_left20 = {{"down",120},{"left",160},{"up",120},{"right",70},{"up",110},{"up",80},{"left",20},{"a",30}},
  talk_right_shop_left40_up30 = {{"down",120},{"left",160},{"up",120},{"right",70},{"up",110},{"up",110},{"left",40},{"up",30},{"a",30}},
  talk_right_shop_left50 = {{"down",120},{"left",160},{"up",120},{"right",70},{"up",110},{"up",110},{"left",50},{"a",30}},
  talk_right_shop_left60_up20 = {{"down",120},{"left",160},{"up",120},{"right",70},{"up",110},{"up",110},{"left",60},{"up",20},{"a",30}},
  enter_left_tent_left100 = {{"down",120},{"left",160},{"up",120},{"left",100},{"up",110},{"a",30}},
  enter_left_tent_left120 = {{"down",120},{"left",160},{"up",120},{"left",120},{"up",110},{"a",30}},
  enter_left_tent_left80_up130 = {{"down",120},{"left",160},{"up",120},{"left",80},{"up",130},{"a",30}},
}
local route = assert(routes[route_id], "unknown route")
local starts, finish = {}, 40
for index, step in ipairs(route) do
  starts[index] = finish
  finish = finish + step[2] + 12
end

local function screenshot(tag)
  local file = assert(io.open(string.format("%s/%s_%s.png", out_dir, route_id, tag), "wb"))
  file:write(emu.takeScreenshot())
  file:close()
end

emu.addMemoryCallback(function()
  if not loaded then loaded = true; emu.loadSavestate(state_data) end
end, emu.callbackType.exec, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addMemoryCallback(function(cpu_address)
  local converted = emu.convertAddress(cpu_address, emu.memType.wsMemory, emu.cpuType.ws)
  if not converted or converted.memType ~= emu.memType.wsPrgRom then return end
  local id = target_by_address[converted.address]
  if id then hits[id] = hits[id] + 1 end
end, emu.callbackType.read, 0, 0xFFFFF, emu.cpuType.ws, emu.memType.wsMemory)

emu.addEventCallback(function()
  local input = {}
  for index, step in ipairs(route) do
    if frame >= starts[index] and frame < starts[index] + step[2] then
      input[step[1]] = true
    end
  end
  if frame >= finish and frame < finish + 360 and frame % 36 < 5 then input.a = true end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  for index, start in ipairs(starts) do
    local stop = start + route[index][2]
    if frame == stop then screenshot(string.format("step%02d", index)) end
  end
  if frame == finish + 420 then
    screenshot("final")
    local file = assert(io.open(string.format("%s/%s.json", out_dir, route_id), "w"))
    file:write(string.format(
      '{"route":"%s","map_a":%d,"map_b":%d,"x":%d,"y":%d,"owned_hits":%d,"buyprice_hits":%d,"repair_hits":%d}\n',
      route_id, emu.read(0x2408, emu.memType.wsWorkRam, false),
      emu.read(0x240B, emu.memType.wsWorkRam, false),
      emu.read(0x245B, emu.memType.wsWorkRam, false),
      emu.read(0x245A, emu.memType.wsWorkRam, false),
      hits.owned, hits.buyprice, hits.repair))
    file:close()
    emu.stop(0)
  end
end, emu.eventType.endFrame)
