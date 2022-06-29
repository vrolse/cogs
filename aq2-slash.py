import json
import logging
import pyrcon
import re
import subprocess
import requests
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from disnake.ext.commands import Context
from helpers import checks


VERSION = 'MC4xMQ== //? h4x by TgT (¬_¬)'
AUTHOR = 'vrol'

logging.basicConfig(level=logging.INFO)

#Need to add lrcon_password and lrconcmds in your cfg to the server. See q2pro servermanual, https://skuller.net/q2pro/nightly/server.html
servername = 'IP'
serverport = 'PORT'
servername2 = 'IP2'
serverport2 = 'PORT2'
rcon_password = 'Use lrcon_password'
rcon_password2 = 'Use lrcon_password'

conn1 = pyrcon.Q2RConnection(servername, serverport, rcon_password)
conn2 = pyrcon.Q2RConnection(servername2, serverport2, rcon_password2)

qs = '/path/to/qstat'

server1 = [qs, '-q2s', servername + ':' + serverport, '-R', '-P', '-sort', 'F', '-json']
server2 = [qs, '-q2s', servername2 + ':' + serverport2, '-R', '-P', '-sort', 'F', '-json']

# Here we name the cog and create a new class for the cog.
class Aq2(commands.Cog, name="AQ2-slash"):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(
        guild_ids=[CHANNELID], #<--ID to the channel where the bot will send to
        name="iinfo",
        description="Pickupbot info.",
    )
    @checks.not_blacklisted()
    async def info(self, context):
        embed = disnake.Embed(
        title="AQ2-pickup",
        description="Bot to check pickup-server and\nmaybe more to come. :)",
        color=0xeee657
        )
        embed.add_field(
        name="Author",
        value=AUTHOR
        )
        embed.add_field(
        name="Bot Version",
        value=VERSION
        )
        await context.send(embed=embed, delete_after=10)

    """AQ2 commands below here"""

    @commands.slash_command(
        guild_ids=[],
        name="status",
        description="Get status from the different servers.",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def status(self, context, check) -> None:
        if not check:
            await context.send("`Use one of the following: server1, server2")
        elif check.lower()=="server1":
            await context.send('```yaml\n{}\n```'.format(conn1.send('status v')))
        elif check.lower()=="server2":
            await context.send('```yaml\n{}\n```'.format(conn2.send('status v')))
        #else:
        #    await context.send(f"`Not found: {check.lower()}, Use one of the following: server1, server2`", delete_after=15)

    @commands.slash_command(
        guild_ids=[CHANNELID], #<--ID to the channel where the bot will send to
        name="changemap",
        description="Change map on the pickup server.",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def changemap(self, context, mapname: str) -> None:
        if mapname is None:
            return await context.send("`You need to write a mapname`")
        conn1.send('gamemap ' + mapname)
        await context.send(f'```yaml\nMap changed to: {mapname}\n```')

    @commands.slash_command(
        guild_ids=[CHANNELID], #<--ID to the channel where the bot will send to
        name="reset",
        description="Reset the server if something is wrong or for fun just to be an asshole 😄",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def reset(self, context, *, server: str = commands.Param(choices={"server1", "server2"})):
        if server == "server1":
            conn1.send('recycle Reset server!')
        elif server == "server2":
            conn2.send('recycle Reset server!')
        await context.send(f'`{server}-server reset by {context.author}!`')

    @commands.slash_command(
        guild_ids=[CHANNELID], #<--ID to the channel where the bot will send to
        name="lrcon",
        description="Send command to server.",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def lrcon(self, context, *, cmd: str) -> None:
        if cmd is None:
            await context.send("`To list all available cmds: use /lrcon list`")
        elif cmd == "list":
            result = conn1.send("listlrconcmds")
            await context.send('```yaml\n{}\n```'.format(result))
        else:
            result = conn1.send(cmd)
            await context.send('```yaml\n{}\n```'.format(result))

    @commands.slash_command(
        guild_ids=[CHANNELID], #<--ID to the channel where the bot will send to
        name="last",
        description="See results from the latest map on server1 or server2.",
    )
    @checks.not_blacklisted()
    #Two different ways to show last scores
    async def last(self, context, result: str = commands.Param(choices={"server1", "server2"})):
        if not result:
            await context.send("`Use server1 or server2`")
        elif result.lower()=='server1':
            url = 'https://your.site.here/file1.txt' #<-- change me!
            response = requests.get(url)
            LastMatch = response.text.splitlines()
            scores = re.match("(.+)> T1 (\d+) vs (\d+) T2 @ (.+)",LastMatch[0])
            nl = "\n"
            if scores:
                MVD2URL = "https://your.site.here/demos" #<-- change me!
                serverName = "ip and port to server" #<-- change me!
                date = scores.group(1)
                t1score = scores.group(2)
                t2score = scores.group(3)
                mapname = scores.group(4)
                embedVar = disnake.Embed(
                    title=':map:    {}    '.format(mapname), 
                    description=date, 
                    color=0xE02B2B,
                    )
                embedVar.set_footer(text=MVD2URL)
                file = disnake.File('./thumbnails/{}.jpg'.format(mapname), filename="map.jpg")
                embedVar.set_thumbnail(url="attachment://map.jpg")
                embedVar.add_field(name='Team Uno', value=t1score)
                embedVar.add_field(name='Team Dos', value=t2score)
                OldMatch = LastMatch
                await context.send(file=file, embed=embedVar)
        elif result.lower()=='server2':
            url = 'https://your.site.here/file2.txt' #<-- change me!
            response = requests.get(url)
            LastMatch = response.text.splitlines()
            scores = re.match("(.+)> T1 (\d+) vs (\d+) T2 @ (.+)",LastMatch[0])
            nl = "\n"
            if scores:
                date = scores.group(1)
                t1score = scores.group(2)
                t2score = scores.group(3)
                mapname = scores.group(4)
                await context.send(f'```json{nl}Date: {date}{nl}Map: {mapname}{nl+nl}Team Uno {t1score} vs {t2score} Team Dos{nl}```')
        else:
            await context.send("`Use server1 or server2`")

    @commands.slash_command(
        guild_ids=[CHANNELID], #<--ID to the channel where the bot will send to
        name="check",
        description="Check server.",
    )
    @checks.not_blacklisted()
    async def check(self, context, server: str = commands.Param(choices={"server1", "server2"})
    ):
        if server is None:
            return await context.send("`Use one of the following: server1, server2`")
        try: 
            if server.lower()=='server1':
                test = server1
            elif server.lower()=='server2':
                test = server2
            scores = []
            s = subprocess.check_output(test)
            data = json.loads(s)
            for te in data:
                print()
            for each in data[0]['players']:
                scores.append("{:>6d} - {}".format(each['score'],each['name']))
            scores = "\n".join(scores)
            nl = '\n'
            await context.send(f"```json{nl}{te['name']}{nl+nl}Map: {te['map']}{nl}Time: {te['rules']['maptime']}{nl+nl}Team1 vs Team2{nl}  {te['rules']['t1']}       {te['rules']['t2']}{nl+nl}Frags:   Players:{nl}{scores}```")
        except KeyError as e:
            print(e)
            await context.send("`Use one of the following: server1, server2`")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.

def setup(bot):
    bot.add_cog(Aq2(bot))
