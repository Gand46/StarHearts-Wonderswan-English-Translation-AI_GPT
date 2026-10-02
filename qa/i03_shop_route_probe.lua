local state_path = assert(os.getenv("MESEN_BASESTATE"))
local out_dir = assert(os.getenv("MESEN_OUTDIR"))
local route_id = assert(os.getenv("MESEN_ROUTE"))
local state_data = assert(io.open(state_path, "rb")):read("*a")
local frame, loaded = 0, false
local hits = {buy = 0, sell = 0, wpn = 0, arm = 0}
local ranges = {
  buy = {0x219432, 0x219434}, sell = {0x21943A, 0x21943D},
  wpn = {0x2192F6, 0x2192F8}, arm = {0x2192FE, 0x219300},
}
local by_address = {}
for id, range in pairs(ranges) do
  for address = range[1], range[2] do by_address[address] = id end
end

local routes = {
  r80_a = {{"right",80},{"a",40}},
  d40_r80_u20_a = {{"down",40},{"right",80},{"up",20},{"a",40}},
  u40_r80_d20_a = {{"up",40},{"right",80},{"down",20},{"a",40}},
  r120_u40_a = {{"right",120},{"up",40},{"a",40}},
  r120_d40_a = {{"right",120},{"down",40},{"a",40}},
  d80_r120_u80_a = {{"down",80},{"right",120},{"up",80},{"a",40}},
}
local route = assert(routes[route_id], "unknown route")
local starts, finish = {}, 40
for index, step in ipairs(route) do
  starts[index] = finish; finish = finish + step[2] + 15
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

emu.addEventCallback(function()
  local input = {}
  for index, step in ipairs(route) do
    if frame >= starts[index] and frame < starts[index] + step[2] then input[step[1]] = true end
  end
  if frame >= finish and frame < finish + 240 and frame % 30 < 5 then input.a = true end
  emu.setInput(input, 0)
end, emu.eventType.inputPolled)

emu.addEventCallback(function()
  frame = frame + 1
  if frame == finish + 300 then
    local image = assert(io.open(out_dir .. "/shop_route_" .. route_id .. ".png", "wb"))
    image:write(emu.takeScreenshot()); image:close()
    local f = assert(io.open(out_dir .. "/shop_route_" .. route_id .. ".json", "w"))
    f:write(string.format(
      '{"route":"%s","map_a":%d,"map_b":%d,"x":%d,"y":%d,"buy_hits":%d,"sell_hits":%d,"wpn_hits":%d,"arm_hits":%d}\n',
      route_id, emu.read(0x2408, emu.memType.wsWorkRam, false),
      emu.read(0x240B, emu.memType.wsWorkRam, false),
      emu.read(0x245B, emu.memType.wsWorkRam, false),
      emu.read(0x245A, emu.memType.wsWorkRam, false),
      hits.buy, hits.sell, hits.wpn, hits.arm))
    f:close(); emu.stop(0)
  end
end, emu.eventType.endFrame)
