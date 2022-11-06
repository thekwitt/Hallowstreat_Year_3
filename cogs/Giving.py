import string
import discord, time, random
from discord import app_commands
from typing import Optional
from discord.ext import commands
from discord.app_commands import  Choice
from extra.discord_functions import extra_functions

class Giving(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  async def cd_check3(interaction: discord.Interaction):
    users = list(interaction.data['resolved']['users'].keys())
    user_raw = interaction.data['resolved']['users'][users[0]]
    user = interaction.guild.get_member(int(user_raw['id']))
    amount_raw = interaction.data['options'][0]
    amount = amount_raw['value']

    if interaction.client.ready == False or interaction.guild.chunked == False:
      return

    if int(user.id) == interaction.user.id:
      return
    elif user.bot == True:
      return

    user_data = await interaction.client.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", interaction.user.id, interaction.guild_id)
    if(len(user_data['candy_bag']) < amount):
      return

    cds = await interaction.client.db_pool.fetchrow("SELECT * FROM command_cooldowns WHERE Guild_ID = $1", interaction.guild_id)

    return app_commands.Cooldown(1, 60 * cds['bulk_give'])


  @app_commands.command(name="bulk_give_candy",description='Give candy to someone in bulk!.')
  @app_commands.describe(amount='The amount of candy you want to give', user='The user you want to give candy to')
  @app_commands.checks.dynamic_cooldown(cd_check3, key=lambda i: (i.guild_id, i.user.id))
  async def bulkgivecandy(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100], user: discord.User) -> None:
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Bulk Give Candy Command Execute')
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
          return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      await extra_functions.beforeCommand(self.bot, interaction)

      settings = await extra_functions.getGuildSettings(self.bot, interaction.guild)

      if settings['enable_giving'] == False:
        return await interaction.response.send_message(content='Giving candy is disabled.')

      # DO CODE BELOW

      if await self.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", user.id, interaction.guild_id) == None:
          await extra_functions.Insert_User(self.bot,interaction.guild.id,user.id)   
      if user.id == interaction.user.id:
        return await interaction.response.send_message(content='You can\'t give candy to yourself!')
      elif user.bot == True:
        return await interaction.response.send_message(content='Bots can\'t eat candy.')
      elif amount > settings['give_limit']:
        return await interaction.response.send_message(content='This server is set for you to only give ' + str(settings['give_limit']) + ' or less.')

      user_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND guild_id = $2", interaction.user.id, interaction.guild_id)
      target_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND guild_id = $2", user.id, interaction.guild_id)

      if(len(user_data['candy_bag']) < amount):
        return await interaction.response.send_message(content='You don\'t have that much candy to give! Please select ' + str(amount) + ' or less candy!')

      for x in range(amount):
        c = random.choice(user_data['candy_bag'])
        user_data['candy_bag'].remove(c)
        target_data['candy_bag'].append(c)

      await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = $1 WHERE member_id = $2 AND guild_id = $3', user_data['candy_bag'], interaction.user.id, interaction.guild_id)
      await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = $1 WHERE member_id = $2 AND guild_id = $3', target_data['candy_bag'], user.id, interaction.guild_id)
      cds = await interaction.client.db_pool.fetchrow("SELECT * FROM command_cooldowns WHERE Guild_ID = $1", interaction.guild_id)
      embed = discord.Embed(title=interaction.user.name + ' gave away a piece of candy!', description='⠀\nThey gave away ' + str(amount) + ' pieces of candy and is now in ' + user.display_name + '\'s bag!\n⠀',color=discord.Color.brand_green()).set_footer(text='You can give another away after ' + str(cds['bulk_give']) + ' minutes.')

      await interaction.response.send_message(embeds=[embed])

  @bulkgivecandy.error
  async def bulkgivecandy_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
      return await interaction.response.send_message("You\'ve used this command recently. Please wait " + str(int(error.retry_after/60)) + " minutes, " + str(int(error.retry_after+1) % 60) + " seconds!", ephemeral=True)


  async def cd_check2(interaction: discord.Interaction):
    users = list(interaction.data['resolved']['users'].keys())
    user_raw = interaction.data['resolved']['users'][users[0]]
    user = interaction.guild.get_member(int(user_raw['id']))

    if interaction.client.ready == False or interaction.guild.chunked == False:
      return

    if int(user.id) == interaction.user.id:
      return
    elif user.bot == True:
      return

    cds = await interaction.client.db_pool.fetchrow("SELECT * FROM command_cooldowns WHERE Guild_ID = $1", interaction.guild_id)

    return app_commands.Cooldown(1, 60 * cds['give'])


  @app_commands.command(name="give_candy",description='Give a piece of candy to someone!.')
  @app_commands.describe(candy='The candy you want to look up.', user='The user you want to give candy to')
  @app_commands.checks.dynamic_cooldown(cd_check2, key=lambda i: (i.guild_id, i.user.id))
  async def give_candy(self, interaction: discord.Interaction, candy: str, user: discord.User) -> None:
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Give Candy Command Execute')
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
          return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      await extra_functions.beforeCommand(self.bot, interaction)

      settings = await extra_functions.getGuildSettings(self.bot, interaction.guild)

      if settings['enable_giving'] == False:
        return await interaction.response.send_message(content='Giving candy is disabled.')

      # DO CODE BELOW

      if await self.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", user.id, interaction.guild_id) == None:
          await extra_functions.Insert_User(self.bot,interaction.guild.id,user.id)   
      if user.id == interaction.user.id:
        return await interaction.response.send_message(content='You can\'t give candy to yourself!')
      elif user.bot == True:
        return await interaction.response.send_message(content='Bots can\'t eat candy.')

      user_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND guild_id = $2", interaction.user.id, interaction.guild_id)
      target_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND guild_id = $2", user.id, interaction.guild_id)

      candy_list = [cc for cc in self.bot.candy if cc['id'] == candy]
      if len(candy_list) == 0:
        return await interaction.response.send_message('Oops! Looks like what you entered wasn\'t correct. Make sure you don\'t change the auto completed prompt discord gives you.', ephemeral=True)

      c = [cc for cc in self.bot.candy if cc['id'] == candy]
      user_data['candy_bag'].remove(int(c[0]['id']))
      target_data['candy_bag'].append(int(c[0]['id']))

      await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = $1 WHERE member_id = $2 AND guild_id = $3', user_data['candy_bag'], interaction.user.id, interaction.guild_id)
      await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = $1 WHERE member_id = $2 AND guild_id = $3', target_data['candy_bag'], user.id, interaction.guild_id)
      cds = await interaction.client.db_pool.fetchrow("SELECT * FROM command_cooldowns WHERE Guild_ID = $1", interaction.guild_id)
      embed = discord.Embed(title=interaction.user.name + ' gave away a piece of candy!', description='⠀\nThey gave away' + c[0]['emoji'] + ' and is now in ' + user.display_name + '\'s bag!\n⠀',color=discord.Color.brand_green()).set_footer(text='You can give another away after ' + str(cds['give']) +' minutes.')

      await interaction.response.send_message(embeds=[embed])

  @give_candy.autocomplete('candy')
  async def give_candy_autocomplete(self, interaction: discord.Interaction, current: str):
    try:
      if self.bot.ready == False:
        return

      if await self.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", interaction.user.id, interaction.guild_id) == None:
          await extra_functions.Insert_User(self.bot,interaction.guild.id,interaction.user.id)   

      user_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND guild_id = $2", interaction.user.id, interaction.guild_id)

      pre_candy_list = [candy for candy in self.bot.candy if (current in candy['id'] or current.lower() in candy['name'].lower()) and int(candy['id']) in user_data['candy_bag']]
      candy_list = []
      for i in range(25):
        try:
          pre_candy_list[i]
        except(KeyError, IndexError, TypeError):
          break

        candy_list.append(pre_candy_list[i])

      if len(candy_list) != 0:
        return [Choice(name=str(candy['id']) + ' | ' + candy['name'], value=str(candy['id'])) for candy in candy_list]
      else:
        return [Choice(name = 'No candy found', value='no')]
    except(KeyError, IndexError, TypeError):
      pass
  
  @give_candy.error
  async def give_candy_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
      return await interaction.response.send_message("You\'ve used this command recently. Please wait " + str(int(error.retry_after/60)) + " minutes, " + str(int(error.retry_after+1) % 60) + " seconds!", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Giving(bot))