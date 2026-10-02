local sfout=assert(os.getenv('MESEN_STATEFILE')); local report=assert(os.getenv('MESEN_LUA_REPORT')); local inState=assert(os.getenv('MESEN_BASESTATE')); local frame=0; local loaded=false; local saved=false
local data=assert(io.open(inState,'rb')):read('*a')
local function loadcb(a,v) if not loaded then loaded=true; emu.loadSavestate(data) end end
local function savecb(a,v) if not saved then local s=emu.createSavestate(); local f=assert(io.open(sfout,'wb'));f:write(s);f:close(); saved=true end end
emu.addMemoryCallback(loadcb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
emu.addEventCallback(function()
 local t={}
 if frame>=20 and frame<170 then t.down=true end
 if frame>=190 and frame<890 then t.left=true end
 if frame>=920 and frame<1620 then t.down=true end
 if frame>=1650 and frame<2050 then t.left=true end
 if frame>=2080 and frame<2230 then t.up=true end
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 frame=frame+1
 if frame==2450 then emu.addMemoryCallback(savecb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory) end
 if saved and frame>2460 then local r=assert(io.open(report,'w'));r:write('saved candidate tent\n');r:close();emu.stop(0) end
end,emu.eventType.endFrame)
