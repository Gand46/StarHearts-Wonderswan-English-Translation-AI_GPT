-- Same P4 synthetic checkpoint for F34/F35. Controller input only; no WRAM/SRAM writes.
local f=assert(io.open(assert(os.getenv('BASESTATE')),'rb'));local state=f:read('*a');f:close()
local loaded=false;local frame=0
emu.addMemoryCallback(function()if not loaded then loaded=true;emu.loadSavestate(state)end end,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
emu.addEventCallback(function()
 local k={}
 if frame>=40 and frame<46 then k.down2=true
 elseif frame>=100 and frame<106 then k.up=true
 elseif frame>=130 and frame<136 then k.right=true
 elseif frame>=160 and frame<166 then k.down=true
 elseif frame>=190 and frame<196 then k.down=true end
 emu.setInput(k,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 frame=frame+1
 if frame==380 then
  local p=assert(io.open(assert(os.getenv('MENU_OUT')),'wb'));p:write(emu.takeScreenshot());p:close()
  emu.stop(0)
 end
end,emu.eventType.endFrame)
