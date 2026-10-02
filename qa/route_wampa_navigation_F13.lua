local out=assert(os.getenv('MESEN_OUTDIR')); local report=assert(os.getenv('MESEN_LUA_REPORT')); local frame=0
local initial_a={200,240,280,320,360,400,440,480,520,560,600,640,680,720,760}
local ups0={820,840,860,880,900,920}; local lefts0={960,980,1000,1020,1040,1060,1080,1100}; local story_a={}; for f=1140,4200,40 do table.insert(story_a,f) end
local downs0={}; for f=6600,7200,20 do table.insert(downs0,f) end; for f=10000,10600,20 do table.insert(downs0,f) end
local villager_a={}; for f=7300,9800,40 do table.insert(villager_a,f) end; local close_event={}; for f=11100,11600,40 do table.insert(close_event,f) end
local function hit(list,f,w) for _,s in ipairs(list) do if f>=s and f<s+(w or 3) then return true end end return false end
local function R(a,b) return frame>=a and frame<b end
emu.addEventCallback(function()
 local t={a=hit(initial_a,frame,3) or hit(story_a,frame,3) or hit(villager_a,frame,3) or hit(close_event,frame,3),up=hit(ups0,frame,3),left=hit(lefts0,frame,3),down=hit(downs0,frame,3)}
 if R(11750,12350) then t.down=true end
 if R(12400,13100) then t.left=true end
 if R(13150,13650) then t.down=true end
 if R(13700,14250) then t.left=true end
 if R(14300,14800) then t.up=true end
 if R(14850,15600) then t.left=true end
 emu.setInput(t,0)
end,emu.eventType.inputPolled)
emu.addEventCallback(function() frame=frame+1; if frame>=11800 and frame<=16000 and frame%200==0 then local f=assert(io.open(string.format('%s/f%05d.png',out,frame),'wb')); f:write(emu.takeScreenshot()); f:close() end; if frame>=16000 then local f=assert(io.open(report,'w')); f:write('done\n');f:close();emu.stop(0) end end,emu.eventType.endFrame)
