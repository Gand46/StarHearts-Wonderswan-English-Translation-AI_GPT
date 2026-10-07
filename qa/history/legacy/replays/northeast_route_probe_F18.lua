local st=assert(os.getenv('MESEN_BASESTATE'));local out=assert(os.getenv('MESEN_OUTDIR'));local mode=assert(os.getenv('MESEN_MODE'));local frame=0;local loaded=false;local data=assert(io.open(st,'rb')):read('*a')
local function cb()if not loaded then loaded=true;emu.loadSavestate(data)end end
emu.addMemoryCallback(cb,emu.callbackType.exec,0,0xFFFFF,emu.cpuType.ws,emu.memType.wsMemory)
local seqs={
 a={{'right',450},{'down',350},{'right',700}},
 b={{'down',300},{'right',850},{'up',350},{'right',500}},
 c={{'right',450},{'down',550},{'right',700},{'up',450}},
 d={{'down',500},{'right',900}},
 e={{'left',250},{'down',400},{'right',1100},{'up',500}}
}
local seq=seqs[mode];local starts={};local tt=30;for i,s in ipairs(seq)do starts[i]=tt;tt=tt+s[2]+40 end
emu.addEventCallback(function()local t={};for i,s in ipairs(seq)do if frame>=starts[i] and frame<starts[i]+s[2] then t[s[1]]=true end end;emu.setInput(t,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()frame=frame+1;if frame%100==0 then local f=assert(io.open(string.format('%s/f%04d.png',out,frame),'wb'));f:write(emu.takeScreenshot());f:close()end;if frame>tt+250 then local f=assert(io.open(out..'/end.png','wb'));f:write(emu.takeScreenshot());f:close();emu.stop(0)end end,emu.eventType.endFrame)
