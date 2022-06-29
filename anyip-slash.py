import json
import logging
import subprocess
import disnake
from disnake.ext.commands import Context
from disnake.ext import commands, tasks
from disnake import ApplicationCommandInteraction, Option, OptionType
from helpers import json_manager, checks

logging.basicConfig(level=logging.INFO)
qs = '/path/to/qstat'

# Here we name the cog and create a new class for the cog.
class anyip(commands.Cog, name="anyip-slash"):
    def __init__(self, bot):
        self.bot = bot

    """AQ2 commands below here"""

    @commands.slash_command(
        guild_ids=[CHANNELID], #<--ID to the channel where the bot will send to
        name="checkip",
        description="Check server by ip or ip:port.",
        options=[
            Option(
                name="ip",
                description="Fill in ip and/or port to the server.",
                type=OptionType.string,
                required=True
            )
        ],
    )
    @checks.not_blacklisted()
    async def checkip(self, interaction: ApplicationCommandInteraction, ip: str = None):
        if ip is None:
            return await interaction.send("`Shiieeeet.. did you forget the IP?!`")
        try:
            test = [qs, '-q2s', '-R', '-P', '-sort', 'F', '-json']
            test.insert(2, '{}'.format(ip))
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
            if 't1' in te['rules']:
                t1 = te['rules']['t1']
            else:
                t1 = "NA"
            if 't2' in te['rules']:
                t2 = te['rules']['t2']
            else:
                t2 = "NA"
            await interaction.send(f"```json{nl}{te['name']}{nl+nl}Map: {te['map']}{nl}Time: {maptajm}{nl+nl}Team1 vs Team2{nl}  {t1}       {t2}{nl+nl}Frags:   Players:{nl}{scores}```")
        except KeyError as e:
            await interaction.send("`Dang it! Invalid IP or not an AQ2-server 🤦‍`")

# And the we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(anyip(bot))
