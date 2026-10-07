local out=assert(os.getenv('MESEN_OUTDIR'));local st=assert(os.getenv('MESEN_BASESTATE'));local sf=assert(os.getenv('MESEN_STATEFILE'));local frame=0;local loaded=false;local saved=false;local data=assert(io.open(st,'rb')):read('*a')
local function cb(a,v)if not loaded then loaded=true;emu.loadSavestate(data)end end
local function scb(a,v)if not saved then local s=emu.createSavestate();local f=assert(io.open(sf,'wb'));f:write(s);f:close();saved=true end end
emu.addMemoryCallback(cb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
emu.addEventCallback(function()local t={}
 if frame>=20 and frame<40 then t.left=true end
 if frame>=70 and frame<470 then t.up=true end
 if frame>=520 and frame<2600 and frame%45<3 then t.a=true end
 emu.setInput(t,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()frame=frame+1;if frame%100==0 then local f=assert(io.open(string.format('%s/f%04d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close()end;if frame==2650 then emu.addMemoryCallback(scb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)end;if saved and frame>2670 then emu.stop(0)end end,emu.eventType.endFrame)
