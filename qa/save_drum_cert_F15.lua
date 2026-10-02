local sf=assert(os.getenv('MESEN_STATEFILE'));local out=assert(os.getenv('MESEN_OUTDIR'));local rep=assert(os.getenv('MESEN_LUA_REPORT'));local frame=0;local loaded=false;local data=assert(io.open(sf,'rb')):read('*a')
local function cb(a,v) if not loaded then loaded=true;emu.loadSavestate(data) end end
emu.addMemoryCallback(cb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
emu.addEventCallback(function()
 local t={}
 if frame>=20 and frame<25 then t.a=true end
 if frame>=160 and frame<180 then t.up2=true end
 if frame>=330 and frame<335 then t.a=true end -- confirm Save progress now?
 if frame>=500 and frame<505 then t.a=true end -- dismiss SAVED if needed
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 frame=frame+1
 if frame>=140 and frame<=620 and frame%20==0 then local f=assert(io.open(string.format('%s/f%04d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close()end
 if frame>=650 then local r=assert(io.open(rep,'w'));r:write('done\n');r:close();emu.stop(0)end
end,emu.eventType.endFrame)
