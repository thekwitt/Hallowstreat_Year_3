import discord
from discord import app_commands, Interaction
from discord.ext import commands
from discord.app_commands import Group
from discord.ext.commands import GroupCog
from discord.app_commands import AppCommandError, Choice
from extra.discord_functions import extra_functions

class Settings(GroupCog, group_name='settings', group_description='Get or Set Settings for the bot on your server!'):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name="changemessagecountfordrop",description='Change the amount of messages it takes for a drop to spawn.')
  @app_commands.describe(message='The message count')
  async def change_message_count_for_drop(self, interaction: discord.Interaction, message: app_commands.Range[int, 1, 100]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_message_count_for_drop Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET Drop_Message_Count = $1 WHERE Guild_ID = $2',message, interaction.guild.id)
      await interaction.response.send_message('The Drop Message Count is now ' + str(message) + ' messages.')

  @app_commands.command(name="change_vc_member_multiple",description='Change the number of people in vc divided by this value to decrement the message count.')
  @app_commands.describe(players='The number of players divided by this value.')
  async def change_vc_member_multiple(self, interaction: discord.Interaction, players: app_commands.Range[int, 1, 100]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_message_count_for_drop Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET vc_member_count = $1 WHERE Guild_ID = $2',players, interaction.guild.id)
      await interaction.response.send_message('The number of players divided by ' + str(players) + ' will decrement 1 message from the message count.\nHow it works is if 6 people are in vc and this value is 3, then it will decrement the messages by two since 6 / 3 is 2.')

  @app_commands.command(name="change_command_cooldown",description='Change a command\'s Cooldown')
  @app_commands.choices(command_name = [Choice(name="/give", value="0"), Choice(name="/bulk_give", value="1"), Choice(name="/scare", value="2")])
  @app_commands.describe(command_name = 'The name of the command you want to change.')
  async def change_command_cooldown(self, interaction: discord.Interaction, command_name: Choice[str], minutes: app_commands.Range[int, 1, 720]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_command_cooldown Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)
      # DO CODE BELOW
      command_name = command_name.value

      if int(command_name) == 0:
        await self.bot.db_pool.execute('UPDATE command_cooldowns SET give = $1 WHERE Guild_ID = $2',minutes, interaction.guild.id)
      elif int(command_name) == 1:
        await self.bot.db_pool.execute('UPDATE command_cooldowns SET bulk_give = $1 WHERE Guild_ID = $2',minutes, interaction.guild.id)
      elif int(command_name) == 2:
        await self.bot.db_pool.execute('UPDATE command_cooldowns SET scare = $1 WHERE Guild_ID = $2',minutes, interaction.guild.id)

      await interaction.response.send_message(['**/give**','**/bulk_give**','**/scare**'][int(command_name)] + " is now set to " + str(minutes) + " minutes.")

  @app_commands.command(name="change_time_interval_for_drop",description='Change the time it takes for drops to spawn.')
  @app_commands.describe(seconds='The seconds it takes for a drop to spawn.')
  async def change_time_interval_for_drop(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 60, 3600]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_time_interval_for_drop Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET Drop_Time_Count = $1 WHERE Guild_ID = $2',seconds, interaction.guild.id)
      await interaction.response.send_message('The Drop Time Requirement is now ' + str(seconds) + ' seconds.')

  @app_commands.command(name="change_drop_duration",description='Change how long a drop lasts.')
  @app_commands.describe(seconds='The seconds of the duration.')
  async def change_drop_duration(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 30, 600]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_drop_duration Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      
      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      if await extra_functions.returnPremiumMessage(self.bot, interaction) == False:
        return

      await self.bot.db_pool.execute('UPDATE guild_settings SET Drop_Duration = $1 WHERE Guild_ID = $2',seconds, interaction.guild.id)
      await interaction.response.send_message('The Drop Duration is now ' + str(seconds) + ' seconds.')

  @app_commands.command(name="experimental_vc_count",description='Enable for players in voice channels to decrement the message count every minute!')
  @app_commands.describe(enable='Enable the experimental feature!')
  async def experimental_vc_count(self, interaction: discord.Interaction, enable: bool):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='enable_giving Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET vc_counter_enable = $1 WHERE Guild_ID = $2',enable, interaction.guild.id)
      await interaction.response.send_message('This feature is now set to ' + str(enable) + '! Please keep in mind that this is a beta feature and may or may not break, if you experience any bugs, please use **/support**.')

  @app_commands.command(name="enable_boss",description='Enable the boss fight event on the server.')
  @app_commands.describe(enable='The state of the event.')
  async def enable_boss(self, interaction: discord.Interaction, enable: bool):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='enable_boss Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET enable_boss = $1 WHERE Guild_ID = $2',enable, interaction.guild.id)
      await interaction.response.send_message('The boss fight is now set to ' + str(enable) + '.')

  @app_commands.command(name="enable_giving",description='Enable the /givecandy command on the server.')
  @app_commands.describe(enable='The state of the command.')
  async def enable_giving(self, interaction: discord.Interaction, enable: bool):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='enable_giving Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET Enable_Giving = $1 WHERE Guild_ID = $2',enable, interaction.guild.id)
      await interaction.response.send_message('The /givecandy command is now set to ' + str(enable) + '.')

  @app_commands.command(name="enable_scare",description='Enable the /scare command on the server.')
  @app_commands.describe(enable='The state of the command.')
  async def enable_scare(self, interaction: discord.Interaction, enable: bool):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Setup Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET Enable_Scare = $1 WHERE Guild_ID = $2',enable, interaction.guild.id)
      await interaction.response.send_message('The /scare command is now set to ' + str(enable) + '.')

  @app_commands.command(name="change_candy_per_drop",description='Change how many pieces of candy users get per drop.')
  @app_commands.describe(candy='The pieces of candy.')
  async def change_candy_per_drop(self, interaction: discord.Interaction, candy: app_commands.Range[int, 1, 10]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_candy_per_drop Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      if await extra_functions.returnPremiumMessage(self.bot, interaction) == False:
        return

      await self.bot.db_pool.execute('UPDATE guild_settings SET Candy_Obtain_Amount = $1 WHERE Guild_ID = $2',candy, interaction.guild.id)
      await interaction.response.send_message('Each drop now has ' + str(candy) + ' pieces of candy.')

  @app_commands.command(name="change_users_per_drop",description='Change how many users can access a drop.')
  @app_commands.describe(users='Users per drop.')
  async def change_users_per_drop(self, interaction: discord.Interaction, users: app_commands.Range[int, 1, 100]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_users_per_drop Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET Candy_Object_Per_Drop = $1 WHERE Guild_ID = $2',users, interaction.guild.id)
      await interaction.response.send_message(str(users) + ' users can now obtain candy from one drop.')

  @app_commands.command(name="change_percent_lost_scare",description='Change the percentage of candy lost when using /scare')
  @app_commands.describe(percent='Percent of the Candy Bag lost on scare.')
  async def change_percent_lost_scare(self, interaction: discord.Interaction, percent: app_commands.Range[int, 1, 20]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_percent_lost_scare Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW

      if await extra_functions.returnPremiumMessage(self.bot, interaction) == False:
        return
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET Candy_Steal_Percent = $1 WHERE Guild_ID = $2',percent, interaction.guild.id)
      await interaction.response.send_message(str(percent) + "'%' of the user\'s candy bag can now be lost on /scare")

  @app_commands.command(name="change_bulk_give_limit",description='Change the limit of a bulk give between 1- 100')
  @app_commands.describe(candy='Number of candy to limit bulk giving to.')
  async def change_bulk_give_limit(self, interaction: discord.Interaction, candy: app_commands.Range[int, 1, 100]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_percent_lost_scare Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW

      if await extra_functions.returnPremiumMessage(self.bot, interaction) == False:
        return
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET give_limit = $1 WHERE Guild_ID = $2',candy, interaction.guild.id)
      await interaction.response.send_message(str(candy) + " pieces of candy is now the bulk give limit!")

  @app_commands.command(name="view_settings",description='View all the settings for your bot')
  async def view_settings(self, interaction: discord.Interaction):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='view_settings Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW

      settings = await extra_functions.getGuildSettings(self.bot, interaction.guild)
      cds = await interaction.client.db_pool.fetchrow("SELECT * FROM command_cooldowns WHERE Guild_ID = $1", interaction.guild_id)

      embed = discord.Embed(title=interaction.guild.name + '\'s Settings Page')
      embed.add_field(name='Current Drop Channel(s)', value= ', '.join(['<#' + str(c) + '>' for c in settings['channel_id']]), inline=False)
      embed.add_field(name='Message Count for Drops', value= str(settings['drop_message_count']) + ' messages', inline=False)
      embed.add_field(name='Time Requirement for Drops', value= str(settings['drop_time_count']) + ' seconds', inline=False)
      embed.add_field(name='Duration of Drops', value= str(settings['drop_duration']) + ' seconds', inline=False)
      embed.add_field(name='Giving Enabled?', value= str(settings['enable_giving']), inline=False)
      embed.add_field(name='Scaring Enabled?', value= str(settings['enable_scare']), inline=False)
      embed.add_field(name='Candy Per Drop', value= str(settings['candy_obtain_amount']) + ' pieces of candy', inline=False)
      embed.add_field(name='Players Per Drop', value= str(settings['candy_object_per_drop']) + ' players', inline=False)
      embed.add_field(name='Scare Candy Percentage', value= str(settings['candy_steal_percent']) + '"%" of the players bag', inline=False)
      embed.add_field(name='Boss Difficulty', value= ['Easy', 'Medium', 'Hard', 'Headless'][settings['boss_difficulty']], inline=False)
      embed.add_field(name='Boss Spawn Chance Percentage', value= str(settings['boss_spawn_ratio']) + '"%" spawn chance', inline=False)
      embed.add_field(name='Candy Spawn Chance Percentage', value= str(100 - settings['boss_spawn_ratio']) + '"%" spawn chance', inline=False)      
      embed.add_field(name='Bulk Give Limit', value= str(settings['give_limit']) + ' pieces of candy', inline=False)
      embed.add_field(name='/give Cooldown', value= str(cds['give']) + ' Minutes', inline=False)
      embed.add_field(name='/bulk_give Cooldown', value= str(cds['bulk_give']) + ' Minutes', inline=False)
      embed.add_field(name='/scare Cooldown', value= str(cds['scare']) + ' Minutes', inline=False)
      await interaction.response.send_message(embed=embed)

  @app_commands.command(name="change_boss_difficulty",description='Change boss difficulty')
  @app_commands.choices(difficulty = [Choice(name="Easy", value="0"), Choice(name="Medium", value="1"), Choice(name="Hard", value="2"), Choice(name="Headless", value="3")])
  @app_commands.describe(difficulty = 'The difficulty of the boss.')
  async def change_boss_difficulty(self, interaction: discord.Interaction, difficulty: Choice[str]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_boss_difficulty Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)
      # DO CODE BELOW
      difficulty = difficulty.value

      await self.bot.db_pool.execute('UPDATE guild_settings SET boss_difficulty = $1 WHERE Guild_ID = $2',int(difficulty), interaction.guild.id)
      await interaction.response.send_message(['Easy', 'Medium', 'Hard', 'Headless'][int(difficulty)] + " Difficulty is now set for the boss.")

  @app_commands.command(name="change_boss_spawn_chance",description='Change the percentage of whether the boss will spawn.')
  @app_commands.describe(percent='The boss spawn chance percentage')
  async def change_boss_spawn_chance(self, interaction: discord.Interaction, percent: app_commands.Range[int, 1, 100]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='change_boss_spawn_chance Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('UPDATE guild_settings SET Boss_Spawn_Ratio = $1 WHERE Guild_ID = $2', percent, interaction.guild.id)
      await interaction.response.send_message(str(percent) + "'%' of the time it will spawn the boss and " + str(100 - percent) + ' of the time it will spawn candy drops.')

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Settings(bot))