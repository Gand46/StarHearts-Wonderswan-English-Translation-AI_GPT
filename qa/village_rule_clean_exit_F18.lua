local out=assert(os.getenv('MESEN_OUTDIR')); local st=assert(os.getenv('MESEN_BASESTATE')); local sf=assert(os.getenv('MESEN_STATEFILE')); local frame=0; local loaded=false; local saved=false; local data=assert(io.open(st,'rb')):read('*a')
local function cb() if not loaded then loaded=true; emu.loadSavestate(data) end end
local function scb() if not saved then local s=emu.createSavestate(); local f=assert(io.open(sf,'wb'));f:write(s);f:close();saved=true end end
emu.addMemoryCallback(cb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
emu.addEventCallback(function() local t={};
  for i=0,6 do local s=80+i*140; if frame>=s and frame<s+5 then t.a=true end end
  if frame>=1080 and frame<1260 then t.down=true end
  emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function() frame=frame+1; if frame%100==0 then local f=assert(io.open(string.format('%s/f%04d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close() end; if frame==1320 then emu.addMemoryCallback(scb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory) end; if saved and frame>1340 then emu.stop(0) end end,emu.eventType.endFrame)
