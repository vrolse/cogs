-- Big up to TgT  <3
-- place this file in pluginsfolder for q2admin and add it also to your config.lua file

local actionDIR = "/path/to/www/"
local curT1 = nil
local curT2 = nil
local timeNicePrint
local fileScores = actionDIR..'scores.txt'
local fileStats = nil

function LogMessage(msg)
        matchOver = string.match(msg,"Match is over.+")
        if matchOver ~= nil then
                curT1 = gi.cvar("t1",'').string
                curT2 = gi.cvar("t2",'').string
                MapName = gi.cvar("mapname",'').string
                time = os.time()
                local timeNice = os.date('%d/%m/%y %H:%M', os.time(os.date('*t')))
                timeNicePrint = timeNice.." > T1 "..curT1.." vs "..curT2.." T2 @ "..MapName.."\n"
                gi.dprintf(timeNicePrint)
                writeScores(timeNicePrint)
                return true
        end
end

function writeScores(scores)
	file = io.open(actionDIR.."scores.txt", "w")
	file:write(scores)
	file:close()
end    

function file_exists(file)
	local f = io.open(file, "rb")
	if f then f:close() end
	return f ~= nil
end

function lines_from(file)
	if not file_exists(file) then return {} end
	lines = {}
	for line in io.lines(file) do
		lines[#lines + 1] = line
	end
	return lines
end

function tablelength(T)
	local count = 0
	for _ in pairs(T) do count = count + 1 end
	return count
end
            
function ClientCommand(client)
	cmd = gi.argv(1)
	if cmd == "!last" then
		local lines = lines_from(fileScores)
		local tCount = tablelength(lines)
 		gi.cprintf(client, PRINT_HIGH, "%s\n",lines[tCount])		                                                                 		
		return true
	end
	return false
end
