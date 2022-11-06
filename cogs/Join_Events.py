import discord
from discord.ext import commands
from extra.discord_functions import extra_functions


class Join_Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        if(self.bot.ready == True):
            if guild.chunked == False:
                self.bot.guild_chunk.append(guild.id)
            settings = await self.bot.db_pool.fetchrow("SELECT * FROM guild_settings WHERE guild_id = $1", guild.id)
            if settings != None:
                self.bot.logger.info(extra_functions.printGuildDetails(guild) + ' - Bot was invited! New Guild!')
            else:
                self.bot.logger.info(extra_functions.printGuildDetails(guild) + ' - Bot was invited! Existing Guild!')


            await self.bot.db_pool.execute("INSERT INTO guild_settings (Guild_ID) VALUES ($1) ON CONFLICT (Guild_ID) DO NOTHING;", guild.id)
            await self.bot.db_pool.execute("INSERT INTO guild_stats (Guild_ID) VALUES ($1) ON CONFLICT (Guild_ID) DO NOTHING;", guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        if(self.bot.ready == True):
            self.bot.logger.info(extra_functions.printGuildDetails(guild) + ' - Bot was removed!')

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.ready = True
        self.bot.logger.info('Ready!')
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Join_Events(bot))