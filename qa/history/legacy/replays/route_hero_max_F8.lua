local out=assert(os.getenv('MESEN_OUTDIR')); local report=assert(os.getenv('MESEN_LUA_REPORT')); local frame=0
local function write(p,d)local f=assert(io.open(p,'wb'));f:write(d);f:close()end
local ps={{180,186,{start=true}},{220,226,{a=true}},{260,266,{a=true}}}; for _,x in ipairs({300,330,360,390,420,450,480,510})do ps[#ps+1]={x,x+5,{a=true}}end; ps[#ps+1]={550,556,{start=true}};ps[#ps+1]={600,606,{a=true}};ps[#ps+1]={650,656,{a=true}}
local caps={180,220,260,300,420,510,550,600,650,700,750};local cap={};for _,x in ipairs(caps)do cap[x]=true end
emu.addEventCallback(function()local st={};for _,p in ipairs(ps)do if frame>=p[1] and frame<=p[2]then for k,v in pairs(p[3])do st[k]=v end end end;emu.setInput(st,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()frame=frame+1;if cap[frame]then write(string.format('%s/f%04d.png',out,frame),emu.takeScreenshot())end;if frame==700 then local t={};for i=0,17 do t[#t+1]=string.format('%02X',emu.read(0xC0DE+i,emu.memType.wsMemory))end;write(out..'/C0DE.txt',table.concat(t,' ')..'\n')end;if frame>=760 then write(report,'PASS hero_max\n');emu.stop(0)end end,emu.eventType.endFrame)
