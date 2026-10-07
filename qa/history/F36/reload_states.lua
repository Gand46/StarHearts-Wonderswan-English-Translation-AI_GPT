-- Reload the four delivered F36 shop checkpoints from CPU callbacks.
local root=assert(os.getenv('QA_ROOT'))
local out=assert(os.getenv('OUT'))
local names={'shop_buy/f0570','shop_buy/f0630','shop_sell/f0570','shop_sell/f0630'}
local index,elapsed,load_pending=1,0,true
local log=assert(io.open(out..'/reload.csv','w'));log:write('state,bytes,result\n')
emu.addMemoryCallback(function()
 if load_pending then
  load_pending=false
  local f=assert(io.open(root..'/'..names[index]..'.mss','rb'));local bytes=f:read('*a');f:close()
  assert(#bytes>1024);emu.loadSavestate(bytes)
  log:write(string.format('%s,%d,LOADED\n',names[index],#bytes));log:flush()
 end
end,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
emu.addEventCallback(function()
 elapsed=elapsed+1
 if elapsed==5 then
  local f=assert(io.open(out..'/'..index..'.png','wb'));f:write(emu.takeScreenshot());f:close()
  if index==#names then log:close();emu.stop(0);return end
  index=index+1;elapsed=0;load_pending=true
 end
end,emu.eventType.endFrame)
