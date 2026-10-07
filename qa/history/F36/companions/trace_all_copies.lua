-- Synthetic native opcode0004 through real game coroutine, no ROM writes.
local out=assert(os.getenv('OUT'));local h=assert(io.open(assert(os.getenv('BASESTATE')),'rb'));local base=h:read('*a');h:close()
local targets=assert(loadfile(assert(os.getenv('TARGETS'))))();local limit=tonumber(os.getenv('LIMIT')or#targets);local mode=os.getenv('EXPECT')or'before'
local log=assert(io.open(out..'/copies.csv','w'));log:write('index,offset,copy_pc,source_reads,expected,actual,result\n')
local frame,loaded,index,armed,done=0,false,0,false,false;local warm=nil;local reads=0;local copyPc='';local start=0;local errors=0
local function w(a,v)emu.write16(a,v,emu.memType.wsWorkRam)end
local function dump(a,n)local s='';for i=0,n-1 do s=s..string.format('%02X',emu.read(a+i,emu.memType.wsWorkRam))end;return s end
emu.addMemoryCallback(function()if not loaded then loaded=true;emu.loadSavestate(base)end end,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
for _,pc in ipairs({0x973c8,0x91fa6})do
 emu.addMemoryCallback(function()if armed and not done then reads=reads+1;copyPc=string.format('%05X',pc)end end,emu.callbackType.exec,pc,pc,emu.cpuType.ws,emu.memType.wsMemory)
end
emu.addMemoryCallback(function()
 if not armed or done then return end
 local actual=dump(0xd2ad,16);local t=targets[index];local expected=t[mode];local pass=actual==expected and reads==8
 if not pass then errors=errors+1 end
 log:write(string.format('%d,0x%06X,%s,%d,%s,%s,%s\n',index,t.offset,copyPc,reads,expected,actual,pass and'PASS'or'FAIL'));log:flush();done=true
end,emu.callbackType.exec,0x931fd,0x931fd,emu.cpuType.ws,emu.memType.wsMemory)
local function inject()
 local t=targets[index];local offset=t.offset
 for i=0,6 do w(0xd24b+i*0x72,0)end
 -- Clear allocator bitmap so each independent native spawn can allocate its graphics.
 for a=0xe81d,0xe84c do emu.write(a,0,emu.memType.wsWorkRam)end
 local di=0x1EBB-4*0x05BF;w(di,0x9000);w(di-2,0x3718);di=di-4;for i=0,6 do w(di-i*2,0)end
 w(0xc048,1);w(0xc04a,di-14);w(0xcacd,(offset&0xffff)-8);w(0xcacf,0x2000);emu.write(0xcaca,offset>>16,emu.memType.wsWorkRam)
 emu.write(0xcac7,0,emu.memType.wsWorkRam);emu.write(0xcac8,0,emu.memType.wsWorkRam)
 w(0xcac3,t.key1);w(0xcac5,t.key2);reads=0;copyPc='';armed=true;done=false;start=frame
end
emu.addEventCallback(function()
 frame=frame+1
 if frame==319 then warm=emu.createSavestate()end
 if frame==320 then index=1;inject()end
 if armed and (done or frame-start>=20)then
  if not done then errors=errors+1;log:write(string.format('%d,0x%06X,,0,,,TIMEOUT\n',index,targets[index].offset));log:flush()end
  armed=false
  if index>=limit then log:close();emu.stop(errors==0 and 0 or 1);return end
  index=index+1;inject()
 end
 if frame>5000 then log:close();emu.stop(2)end
end,emu.eventType.endFrame)
