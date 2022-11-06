import discord, json, extra.discord_functions,time
from glob2 import glob
from importlib import reload
from typing import List, Optional, Literal
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Greedy, Context

from extra.discord_functions import extra_functions
from extra.candySpawner import SpawnCandy
from extra.bossSpawnerHard import SpawnBoss

class Sync(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        

        
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.command()
    @commands.is_owner()
    async def recog(self, ctx: Context) -> None:
        self.bot.ready = False
        await ctx.send(f"Commands are recogging")
        extensions = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]
        self.bot.dedicated_patreon = json.load(open('./JSON/premium.json'))
        reload(extra.discord_functions)
        reload(extra.candySpawner)
        reload(extra.bossSpawnerHard)
        for extension in extensions:
            self.bot.logger.info(str(extension) + ' recogging')
            try:
                await ctx.bot.reload_extension(f"cogs.{extension}")
                self.bot.logger.info(str(extension) + ' recogged')
            except Exception as e:
                self.bot.logger.error(str(e) + " for recoggers")
                try:
                    await ctx.bot.reload_extension(f"cogs.{extension[7:]}")
                    self.bot.logger.info(str(extension) + ' recogged')
                except Exception as e:
                    self.bot.logger.error(str(e) + " for recoggers")
        await ctx.send(f"Commands are done recogging")
        c = json.load(open('./JSON/candy.json'))
        self.bot.candy = [ca for ca in c['candy'] if ca['type'] != '']
        self.bot.ready = True

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sync(bot))