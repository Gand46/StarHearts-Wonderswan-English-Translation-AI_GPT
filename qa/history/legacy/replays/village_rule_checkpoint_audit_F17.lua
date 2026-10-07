-- F17 diagnostic: load the F16 navigation state and demonstrate that it resumes
-- inside the gravekeeper conversation. This script is evidence only; do not use
-- the resulting state as a progression checkpoint.
local out=assert(os.getenv('MESEN_OUTDIR')); local st=assert(os.getenv('MESEN_BASESTATE'))
local frame=0; local loaded=false; local data=assert(io.open(st,'rb')):read('*a')
local function cb() if not loaded then loaded=true; emu.loadSavestate(data) end end
emu.addMemoryCallback(cb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
emu.addEventCallback(function()
  local t={}
  if frame<1200 and frame%110<5 then t.a=true end
  if frame>=1200 and frame<2200 then t.down=true end
  emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
  frame=frame+1
  if frame%200==0 then local f=assert(io.open(string.format('%s/f%04d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close() end
  if frame>=2400 then emu.stop(0) end
end,emu.eventType.endFrame)
