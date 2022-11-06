from code import interact
import time
import discord, random, asyncio
from discord.ext.tasks import loop
from discord import app_commands
from discord.ext import commands
from typing import List
from extra.discord_functions import extra_functions
from extra.candySpawner import SpawnCandy
from extra.bossSpawnerHard import SpawnBoss


class candySpawner(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    
  @commands.Cog.listener("on_message")
  async def spawner(self, message):
    if message.guild == None:
      return

    if message.guild.chunked == False and not message.guild.id in self.bot.guild_chunk and not message.guild.id in self.bot.chunked:#if bot.ready == False or not interaction.guild_id in bot.ready_guilds:
      return self.bot.guild_chunk.append(message.guild.id)

    if(message.author.id != self.bot.user.id and message.guild and message.author.bot == False):
      if await extra_functions.setupCheck(self.bot, message.guild) == False:
        return
      else:
        if not str(message.guild.id) in list(self.bot.messages.keys()):
          return await extra_functions.reloadMessageDrop(bot=self.bot, guild=message.guild)
        messageSpawn = self.bot.messages[str(message.guild.id)]

        if messageSpawn['timestamp'] < time.time() and messageSpawn['messageCount'] <= 1 and messageSpawn['activeMessage'] == False:
          try:
            settings = await extra_functions.getGuildSettings(self.bot, message.guild)
            if settings['enable_boss'] == True:
              rand = random.randint(0,100)
              if settings['boss_spawn_ratio'] >= rand:
                await SpawnBoss.spawnBoss(self, message)
              else:
                await SpawnCandy.spawnCandy(self, message)
            else:
                await SpawnCandy.spawnCandy(self, message)
          except Exception as e:
            self.bot.logger(await extra_functions.printGuildDetails(message.guild) + ' | Message Event Fail | ' + str(e))
            return await extra_functions.reloadMessageDrop(bot=self.bot, guild=message.guild)

        elif messageSpawn['activeMessage'] == False:
          self.bot.messages[str(message.guild.id)]['messageCount'] -= 1

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(candySpawner(bot))