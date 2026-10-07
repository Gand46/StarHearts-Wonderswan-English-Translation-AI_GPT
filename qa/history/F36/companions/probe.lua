local out=assert(os.getenv('OUT'));local h=assert(io.open(assert(os.getenv('BASESTATE')),'rb'));local base=h:read('*a');h:close()
local log=assert(io.open(out..'/trace.txt','w'));local f=0;local loaded=false;local injected=false
local offset=tonumber(os.getenv('OFFSET')or'195816',16)
local function w(a,v)emu.write16(a,v,emu.memType.wsWorkRam)end
local function dump(a,n)local s='';for i=0,n-1 do s=s..string.format('%02X',emu.read(a+i,emu.memType.wsWorkRam))end;return s end
emu.addMemoryCallback(function()if not loaded then loaded=true;emu.loadSavestate(base)end end,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
for _,pc in ipairs({0x931f8,0x90eda,0x973c8,0x91fa6,0x931fd,0x9e906,0x9e929,0xAB7DE,0x93564})do
 emu.addMemoryCallback(function()if injected then local s=emu.getState();log:write(string.format('EXEC f=%d pc=%05X ES:SI=%04X:%04X DI=%04X name=%s\n',f,pc,s['cpu.es'],s['cpu.si'],s['cpu.di'],dump(0xd2ad,16)..' keys='..dump(0xcac3,4)..' actor='..dump(0xd24b,8)));log:flush()end end,emu.callbackType.exec,pc,pc,emu.cpuType.ws,emu.memType.wsMemory)
end
emu.addEventCallback(function()local k={};if f%40<5 then k.a=true end;emu.setInput(k,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 f=f+1
 if f==320 then
  for i=0,6 do w(0xd24b+i*0x72,0)end
  local di=0x1EBB-4*0x05BF;w(di,0x9000);w(di-2,0x3718);di=di-4;for i=0,6 do w(di-i*2,0)end
  w(0xC048,1);w(0xC04A,di-14);w(0xCACD,(offset&0xffff)-8);w(0xCACF,0x2000);emu.write(0xCACA,offset>>16,emu.memType.wsWorkRam)
  emu.write(0xC2,offset>>16,emu.memType.wsPort);emu.write(0xCAC7,0,emu.memType.wsWorkRam);emu.write(0xCAC8,0,emu.memType.wsWorkRam)
  w(0xcac3,emu.read16(offset-6,emu.memType.wsPrgRom));w(0xcac5,emu.read16(offset-4,emu.memType.wsPrgRom));w(0xf318,emu.read16(0xf318,emu.memType.wsWorkRam)&0xff7f)
  injected=true
 end
 if f==800 then local h=assert(io.open(out..'/screen.png','wb'));h:write(emu.takeScreenshot());h:close()end
 if f==850 then log:write('DONE name='..dump(0xd2ad,16)..'\n');log:close();emu.stop(0)end
end,emu.eventType.endFrame)
