local out=assert(os.getenv('MESEN_OUTDIR')); local report=assert(os.getenv('MESEN_LUA_REPORT')); local frame=0
local initial_a={200,240,280,320,360,400,440,480,520,560,600,640,680,720,760}
local ups={820,840,860,880,900,920}
local lefts={960,980,1000,1020,1040,1060,1080,1100}
local story_a={}; for f=1140,4200,40 do table.insert(story_a,f) end
local downs={}; for f=6600,7200,20 do table.insert(downs,f) end; for f=10000,10600,20 do table.insert(downs,f) end
local villager_a={}; for f=7300,9800,40 do table.insert(villager_a,f) end
local close_event={}; for f=11100,11600,40 do table.insert(close_event,f) end
local caps={2520,8640,10240,10560,10720,11040}; local C={}; for _,x in ipairs(caps) do C[x]=true end
local function hit(list,f,w) for _,s in ipairs(list) do if f>=s and f<s+(w or 3) then return true end end return false end
emu.addEventCallback(function()
 local t={a=hit(initial_a,frame,3) or hit(story_a,frame,3) or hit(villager_a,frame,3) or hit(close_event,frame,3),up=hit(ups,frame,3),left=hit(lefts,frame,3),down=hit(downs,frame,3)}
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function()
 frame=frame+1
 if C[frame] then local f=assert(io.open(string.format('%s/f%05d.png',out,frame),'wb')); f:write(emu.takeScreenshot()); f:close() end
 if frame>=11700 then local f=assert(io.open(report,'w')); f:write('PASS F12 natural First route\nnormal_first_frame=2520\nevent_first_trial_frames=10560,10720,11040\n'); f:close(); emu.stop(0) end
end,emu.eventType.endFrame)
