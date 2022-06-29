"""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.0.1
"""

import json
import os
import time
import sys
import configparser
import logging
import pyrcon
import re
import subprocess
import requests
import disnake
import helpers
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from disnake.ext.commands import Context
from helpers import checks

VERSION = 'MC4xMQ== //? h4x by TgT (¬_¬)'
AUTHOR = 'vrol'

logging.basicConfig(level=logging.INFO)

servername = IP
serverport = PORT
servername2 = IP2
serverport2 = PORT2
rcon_password = PASSWORD
rcon_password2 = PASSWORD2

conn = pyrcon.Q2RConnection(servername, serverport, rcon_password)
conn2 = pyrcon.Q2RConnection(servername2, serverport2, rcon_password2)

qs = '/path/to/qstat'
server1 = [qs, '-q2s', servername + ':' + serverport, '-R', '-P', '-sort', 'F', '-json']
server2 = [qs, '-q2s', servername2 + ':' + serverport2, '-R', '-P', '-sort', 'F', '-json']

# Here we name the cog and create a new class for the cog.
class Aq2(commands.Cog, name="AQ2-normal"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name="info",
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
        await context.send(embed=embed)

    """AQ2 commands below here"""

    @commands.command(
        name="status",
        description="Get status from the different servers.",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def status(self, context, msg=None):
        if not msg:
            await context.send("`Use one of the following: server1, server2`")
        elif msg.lower()=="server1":
            await context.send('```yaml\n{}\n```'.format(conn.send('status')))
        elif msg.lower()=="server2":
            await context.send('```yaml\n{}\n```'.format(conn2.send('status')))
        else:
            await context.send(f"`Not found: {msg.lower()}, Use one of the following: server1, server2`")

    @commands.command(
        name="cmap",
        description="Change map on the pickup server.",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def cmap(self, context, mapname: str = None):
        if mapname is None:
            return await context.send("`You need to write a mapname`")
        conn.send('gamemap ' + mapname)
        await context.send('```yaml\nMap changed to: {}\n```'.format(mapname))

    @commands.command(
        name="reset",
        description="Reset the server if something is wrong or for fun just to be an asshole 😄",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def reset(self, context):
        conn.send('recycle Reset server!')
        await context.send('`Server reset!`')

    @commands.command(
        name="c",
        description="Send command to server.",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def c(self, context, *, arg: str = None):
        if arg is None:
            return await context.send("`You need to type a cmd after !c\nAvailable cmds: recycle, status, kick, gamemap, serverinfo`")
        result = server1.send(arg)
        await context.send('```yaml\n{}\n```'.format(result))

    @commands.command(
        name="last",
        description="See last map results for pickup or cw server.",
    )
    @checks.not_blacklisted()
    async def last(self, context, sc=None):
        if not sc:
            await context.send("`Use pickup or cw`")
        elif sc.lower()=='pickup':
            url = 'https://your.site.here'
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
        elif sc.lower()=='cw':
            url = 'https://your.site.here'
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
            await context.send("`Use pickup or cw`")

    @commands.command(
        name="check",
        description="Check server.",
    )
    @checks.not_blacklisted()
    async def check(self, context, qt: str = None):
        if qt is None:
            return await context.send("`Use one of the following: server1, server2..`")
        try: 
            if qt.lower()=='pickup':
                test = server1
            elif qt.lower()=='cw':
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
            await context.send("`Use one of the following: server1, server2..`")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.

def setup(bot):
    bot.add_cog(Aq2(bot))
