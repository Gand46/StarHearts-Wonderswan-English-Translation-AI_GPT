local st=assert(os.getenv('MESEN_BASESTATE'));local out=assert(os.getenv('MESEN_OUTDIR'));local mode=assert(os.getenv('MESEN_MODE'));local frame=0;local loaded=false;local data=assert(io.open(st,'rb')):read('*a')
local function cb()if not loaded then loaded=true;emu.loadSavestate(data)end end
emu.addMemoryCallback(cb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
local seqs={a={{'down',170},{'right',110}},b={{'right',110},{'down',180}},c={{'down',220},{'right',160}},d={{'down',130},{'right',170},{'down',80}},e={{'right',160},{'down',230},{'left',60}}}
local seq=seqs[mode];local starts={};local tt=30;for i,s in ipairs(seq)do starts[i]=tt;tt=tt+s[2]+25 end
emu.addEventCallback(function()local t={};for i,s in ipairs(seq)do if frame>=starts[i] and frame<starts[i]+s[2] then t[s[1]]=true end end;if frame>=tt-180 and frame<tt+350 and frame%14<5 then t.a=true end;emu.setInput(t,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()frame=frame+1;if frame%40==0 then local f=assert(io.open(string.format('%s/f%04d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close()end;if frame>tt+400 then local f=assert(io.open(out..'/end.png','wb'));f:write(emu.takeScreenshot());f:close();emu.stop(0)end end,emu.eventType.endFrame)
