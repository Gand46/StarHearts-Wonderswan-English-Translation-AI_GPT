local out=assert(os.getenv('MESEN_OUTDIR'));local sf=assert(os.getenv('MESEN_STATEFILE'));local report=assert(os.getenv('MESEN_LUA_REPORT'));local frame=0;local loaded=false;local data=assert(io.open(sf,'rb')):read('*a')
local function cb(a,v) if not loaded then loaded=true;emu.loadSavestate(data) end end
emu.addMemoryCallback(cb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
emu.addEventCallback(function()
 local t={}
 if frame>=20 and frame<60 then t.left=true end
 if frame>=80 and frame<170 then t.up=true end
 if frame>=200 and frame<2600 and frame%35<3 then t.a=true end
 if frame>=2700 and frame<2706 then t.down2=true end
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function() frame=frame+1;if frame>=1400 and frame<=2800 and frame%100==0 then local f=assert(io.open(string.format('%s/f%04d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close() end;if frame>=3200 then local r=assert(io.open(report,'w'));r:write('done\n');r:close();emu.stop(0) end end,emu.eventType.endFrame)
