-- F37 controlled prompt graphics QA: restore synthetic P4 map state, seed native event coroutine.
-- No ROM writes. Inventory fixture serves only to open category list.
local out=assert(os.getenv('OUT'));local h=assert(io.open(assert(os.getenv('BASESTATE')),'rb'));local base=h:read('*a');h:close()
local target=tonumber(assert(os.getenv('PROMPT')));assert(target==12 or target==13 or target==14 or target==17);local replaced=false;local frame,loaded=0,false;local save_request=nil;local mode=os.getenv('MODE')or'sell';local log=assert(io.open(out..'/trace.txt','w'))
local function w(a,v)emu.write16(a,v,emu.memType.wsWorkRam)end
local function snap(n)local f=assert(io.open(out..'/'..n..'.png','wb'));f:write(emu.takeScreenshot());f:close()end
emu.addMemoryCallback(function()if not loaded then loaded=true;emu.loadSavestate(base)end
 if save_request then local name=save_request;save_request=nil;local data=emu.createSavestate();assert(#data>1024,'empty savestate');local h=assert(io.open(out..name,'wb'));h:write(data);h:close()end
end,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
for tag,pc in pairs({shop=0x9BD30,stock=0x9CEB0,buy_callback=0x9CFF0,sell_callback=0x9D026,buy_panel=0xAA040,sell_panel=0xAA4E0})do
 emu.addMemoryCallback(function()if frame>300 then log:write(tag..' frame='..frame..'\n');log:flush()end end,emu.callbackType.exec,pc,pc,emu.cpuType.ws,emu.memType.wsMemory)
end
emu.addMemoryCallback(function()
 if frame>300 then local s=emu.getState();if s['cpu.es']==0x2000 and s['cpu.si']==0x843E and s['cpu.cx']==15 and s['cpu.di']==0x4FC0 then assert(not replaced);replaced=true;s['cpu.cx']=target;emu.setState(s);log:write('ACCESS_METHOD=POINTER_INJECTION; native common prompt selector15 -> '..target..'; no ROM or decoded-VRAM writes; visual-only test, no action confirmation\n');log:flush()end;log:write(string.format('DECODE f=%d ES:SI=%04X:%04X CX=%04X DS:DI=%04X:%04X\n',frame,s['cpu.es'],s['cpu.si'],s['cpu.cx'],s['cpu.ds'],s['cpu.di']));log:flush()end
end,emu.callbackType.exec,0xA254C,0xA254C,emu.cpuType.ws,emu.memType.wsMemory)
local function pulse(t)return frame>=t and frame<t+5 end
emu.addEventCallback(function()
 local k={};if pulse(360)or pulse(405)or pulse(450)or pulse(510)or pulse(620)then k.a=true end
 if mode=='sell'and pulse(490)then k.down=true end
 emu.setInput(k,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 frame=frame+1
 if frame==320 then
  local di=0x1EBB-4*0x05BF;w(di,0x9000);w(di-2,0x3718);di=di-4;for i=0,6 do w(di-i*2,0)end
  w(0xC048,1);w(0xC04A,di-14);w(0xCACD,0x6CA4);w(0xCACF,0x2000);emu.write(0xCACA,0x1A,emu.memType.wsWorkRam)
  emu.write(0xCAC7,0,emu.memType.wsWorkRam);emu.write(0xCAC8,0,emu.memType.wsWorkRam)
  w(0xC150,0x0018);w(0xC152,1)
  log:write('ACCESS_METHOD=WRAM_POKE; detail=SYNTHETIC_NATIVE_EVENT_COROUTINE; bank1A script6CA4; inventory C150 item0018 qty1; no ROM writes\n');log:flush()
 end
 if frame>=330 and frame%30==0 then snap(string.format('f%04d',frame))end
 if frame==630 then save_request=string.format('/f%04d.mss',frame)end
 if frame>=660 then assert(replaced,'target decode not reached');log:close();emu.stop(0)end
end,emu.eventType.endFrame)
