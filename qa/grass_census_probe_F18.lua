local st=assert(os.getenv('MESEN_BASESTATE'));local out=assert(os.getenv('MESEN_OUTDIR'));local frame=0;local loaded=false;local data=assert(io.open(st,'rb')):read('*a')
local function cb()if not loaded then loaded=true;emu.loadSavestate(data)end end
emu.addMemoryCallback(cb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
local seq={{'down',120},{'left',500},{'down',80},{'right',900},{'down',80},{'left',900},{'down',80},{'right',900},{'up',70},{'left',900},{'up',70},{'right',900}}
local starts={};local tt=30;for i,s in ipairs(seq)do starts[i]=tt;tt=tt+s[2]+20 end
emu.addEventCallback(function()local t={};for i,s in ipairs(seq)do if frame>=starts[i] and frame<starts[i]+s[2] then t[s[1]]=true end end;if frame>=30 and frame<tt and frame%16<5 then t.a=true end;emu.setInput(t,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()frame=frame+1;if frame%150==0 then local f=assert(io.open(string.format('%s/f%05d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close()end;if frame>tt+300 then local f=assert(io.open(out..'/end.png','wb'));f:write(emu.takeScreenshot());f:close();emu.stop(0)end end,emu.eventType.endFrame)
