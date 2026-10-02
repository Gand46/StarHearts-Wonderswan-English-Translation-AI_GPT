local out=assert(os.getenv('MESEN_OUTDIR')); local report=assert(os.getenv('MESEN_LUA_REPORT')); local frame=0
local function write(p,d)local f=assert(io.open(p,'wb'));f:write(d);f:close()end
local ps={{180,186,{start=true}},{220,226,{a=true}},{260,266,{a=true}}};for _,x in ipairs({300,330,360,390,420,450,480,510})do ps[#ps+1]={x,x+5,{a=true}}end;ps[#ps+1]={550,556,{start=true}};ps[#ps+1]={600,606,{a=true}};ps[#ps+1]={650,656,{a=true}};ps[#ps+1]={800,806,{down2=true}};ps[#ps+1]={900,903,{right=true}};for _,x in ipairs({950,1000,1050,1100,1150,1200})do ps[#ps+1]={x,x+3,{down=true}}end;ps[#ps+1]={1250,1254,{a=true}}
local caps={1220,1270,1320,1400};local cap={};for _,x in ipairs(caps)do cap[x]=true end
emu.addEventCallback(function()local st={};for _,p in ipairs(ps)do if frame>=p[1]and frame<=p[2]then for k,v in pairs(p[3])do st[k]=v end end end;emu.setInput(st,0)end,emu.eventType.inputPolled)
emu.addEventCallback(function()frame=frame+1;if cap[frame]then write(string.format('%s/f%04d.png',out,frame),emu.takeScreenshot())end;if frame>=1400 then write(report,'PASS options\n');emu.stop(0)end end,emu.eventType.endFrame)
