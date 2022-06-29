import json
import sys
import logging
import pyrcon
import subprocess
import requests
from disnake.ext import commands
from disnake.ext.commands import Context
from disnake.ext import commands, tasks
from helpers import checks

logging.basicConfig(level=logging.INFO)

qs = '/path/to/qstat'


# Here we name the cog and create a new class for the cog.
class anyip(commands.Cog, name="anyip-normal"):
    def __init__(self, bot):
        self.bot = bot

    """AQ2 commands below here"""

    @commands.command(
        name="checkip",
        description="Check server by ip or ip:port.",
    )
    @checks.not_blacklisted()
    async def checkip(self, context, qt: str = None):
        if qt is None:
            return await context.send("`Shiieeeet.. did you forget the IP?!`")
        try:
            test = [qs, '-q2s', '-R', '-P', '-sort', 'F', '-json']
            test.insert(2, '{}'.format(qt))
            scores = []
            s = subprocess.check_output(test)
            data = json.loads(s)
            for te in data:
                print()
            for each in data[0]['players']:
                scores.append("{:>6d} - {}".format(each['score'],each['name']))
            scores = "\n".join(scores)
            nl = '\n'
            if 'maptime' in te['rules']:
                maptajm = te['rules']['maptime']
            else:
                maptajm = "0"
            await context.send(f"```json{nl}{te['name']}{nl+nl}Map: {te['map']}{nl}Time: {maptajm}{nl+nl}Team1 vs Team2{nl}  {te['rules']['t1']}       {te['rules']['t2']}{nl+nl}Frags:   Players:{nl}{scores}```")
        except KeyError as e:
            await context.send("`Dang it! Invalid IP or not an AQ2-server 🤦‍`")

# And the we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(anyip(bot))
