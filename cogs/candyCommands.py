import string
import discord, time, random
from discord import app_commands
from typing import Optional
from discord.ext import commands
from discord.app_commands import  Choice
from extra.discord_functions import extra_functions

class Links(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Topgg Vote Link', url='https://top.gg/bot/886391809939484722/vote'))

class CandyCommands(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    
  @app_commands.command(name="candy_lookup",description='Look up a piece of candy')
  @app_commands.describe(candy='The candy you want to look up.')
  async def candy_lookup(self, interaction: discord.Interaction, candy: str) -> None:
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Candy Lookup Command Execute')
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
          return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW

      candy_list = [cc for cc in self.bot.candy if cc['id'] == candy]
      if len(candy_list) == 0:
        return await interaction.response.send_message('Oops! Looks like what you entered wasn\'t correct. Make sure you don\'t change the auto completed prompt discord gives you.', ephemeral=True)

      c = [cc for cc in self.bot.candy if cc['id'] == candy][0]
      emoji = self.bot.get_emoji(int(c['emoji_id']))
      embed = discord.Embed(title=c['name'],color=discord.Color.greyple()).set_footer(text='Check out other candies you\'ve collected!')
      embed.set_image(url=emoji.url)
      embed.add_field(name='Bonus - ' + ['Collector Mask','Second Wind','Backstab','Mental Shield','The Ugly','Power Up','Golden Collector Mask','Golden Second Wind','Golden Backstab','Golden Mental Shield','The Golden Ugly','Golden Power Up'][c['bonus']], value='When eaten: **' + ['Get a bonus on collecting from a candy message.','Get a second chance on collecting a candy message if you fail the first time','If you get scared, you have a chance to steal some candy back','Have a higher chance to defend against a scare','Get a bigger bonus on scaring people','Deal bonus damage to the Headless Horseman', 'Get a massive bonus on collecting from a candy message.','Get a second chance on collecting the candy message if you fail the first time','If you get scared, you have a chance to steal alot of candy back','Have a even higher chance to defend against a scare','Greatly get a bigger bonus on scaring people','Greatly Deal bonus damage to the Headless Horseman'][c['bonus']] + '**')

      await interaction.response.send_message(embeds=[embed])

  @candy_lookup.autocomplete('candy')
  async def candy_lookup_autocomplete(self, interaction: discord.Interaction, current: str):
    try:
      if self.bot.ready == False:
        return

      pre_candy_list = [candy for candy in self.bot.candy if current in candy['id'] or current.lower() in candy['name'].lower()]
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
    except:
      pass

  @app_commands.command(name="candy_bonus_list",description='All the bonuses!')
  @app_commands.choices(bonus = [Choice(name="Collector Mask", value="0"), Choice(name="Second Wind", value="1"), Choice(name="Backstab", value="2"), Choice(name="Mental Shield", value="3"), Choice(name="The Ugly", value="4"), Choice(name="Power Up", value="5")])
  async def candybonuslist(self, interaction: discord.Interaction, bonus: Choice[str]) -> None:
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Candy Lookup Command Execute')
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
          return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW

      bonus = int(bonus.value)
      embed = discord.Embed(title= ['Collector Mask','Second Wind','Backstab','Mental Shield','The Ugly','Power Up'][bonus] + ' Candy Bonus List',description= ['Get a bonus on collecting from a candy message.','Get a second chance on collecting a candy message if you fail the first time','If you get scared, you have a chance to steal some candy back','Have a higher chance to defend against a scare','Get a bigger bonus on scaring people','Deal bonus damage to the Headless Horseman', 'Get a massive bonus on collecting from a candy message.','Get a second chance on collecting the candy message if you fail the first time','If you get scared, you have a chance to steal alot of candy back','Have a even higher chance to defend against a scare','Greatly get a bigger bonus on scaring people','Greatly Deal bonus damage to the Headless Horseman'][bonus], color=discord.Color.orange())
      embed.set_footer(text='Use /eatcandy to get one of these bonuses!')

      temp_array = [c for c in self.bot.candy if c['bonus'] == bonus]
      temp_collect = []
      temp_int = 0
      for temp in temp_array:
          temp_collect.append(temp['emoji'])

          temp_int += 1
          if temp_int >= 20:
              embed.add_field(name=['Collector Mask','Second Wind','Backstab','Mental Shield','The Ugly','Power Up'][bonus], value=' '.join(temp_collect), inline=False)
              temp_collect = []
              temp_int = 0
      embed.add_field(name=['Collector Mask','Second Wind','Backstab','Mental Shield','The Ugly','Power Up'][bonus], value=' '.join(temp_collect), inline=False) 
          
      await interaction.response.send_message(embeds=[embed])

  @app_commands.command(name="candy_golden_bonus_list",description='All the bonuses!')
  async def candygoldenbonuslist(self, interaction: discord.Interaction) -> None:
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Golden Candy Lookup Command Execute')
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
          return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW

      embed = discord.Embed(title= 'Candy Bonus List', color=discord.Color.orange())
      embed.set_footer(text='Use /eatcandy to get one of these bonuses!')

      for t in range(6, 12):
          temp_array = [c for c in self.bot.candy if c['bonus'] == t]
          temp_collect = []
          temp_int = 0
          for temp in temp_array:
              temp_collect.append(temp['emoji'])

              temp_int += 1
              if temp_int >= 20:
                  embed.add_field(name=['Golden Collector Mask','Golden Second Wind','Golden Backstab','Golden Mental Shield','The Golden Ugly','Golden Power Up'][t-6], value=' '.join(temp_collect), inline=False)
                  temp_collect = []
                  temp_int = 0
          embed.add_field(name=['Golden Collector Mask','Golden Second Wind','Golden Backstab','Golden Mental Shield','The Golden Ugly','Golden Power Up'][t-6], value=' '.join(temp_collect), inline=False) 

      await interaction.response.send_message(embed=embed)

  @app_commands.command(name="eat_candy",description='Eat a piece of candy and get a bonus.')
  @app_commands.describe(candy='The candy you want to look up.')
  async def eat_candy(self, interaction: discord.Interaction, candy: str) -> None:
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Eat Candy Command Execute')
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
          return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW

      user_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND guild_id = $2", interaction.user.id, interaction.guild_id)

      candy_list = [cc for cc in self.bot.candy if cc['id'] == candy]
      if len(candy_list) == 0:
        return await interaction.response.send_message('Oops! Looks like what you entered wasn\'t correct. Make sure you don\'t change the auto completed prompt discord gives you.', ephemeral=True)

      c = [cc for cc in self.bot.candy if cc['id'] == candy]
      extra_functions.logUseInfo(self.bot,interaction.user,interaction.guild, str(c))
      user_data['candy_bag'].remove(int(c[0]['id']))
      timestamp = time.time() + 3600
      await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = $1, eat_bonus = $4, eat_expire = $5 WHERE member_id = $2 AND guild_id = $3', user_data['candy_bag'], interaction.user.id, interaction.guild_id, c[0]['bonus'], timestamp)
      embed = discord.Embed(title=interaction.user.name + ' ate a piece of candy!', description='You gained the bonus **' + ['Collector Mask','Second Wind','Backstab','Mental Shield','The Ugly','Power Up','Golden Collector Mask','Golden Second Wind','Golden Backstab','Golden Mental Shield','The Golden Ugly','Golden Power Up'][c[0]['bonus']] + '!**\n\nThis will give you the bonus effect of: "' + ['Get a bonus on collecting from a candy message.','Get a second chance on collecting a candy message if you fail the first time','If you get scared, you have a chance to steal some candy back','Have a higher chance to defend against a scare','Get a bigger bonus on scaring people','Deal bonus damage to the Headless Horseman', 'Get a massive bonus on collecting from a candy message.','Get a second chance on collecting the candy message if you fail the first time','If you get scared, you have a chance to steal alot of candy back','Have a even higher chance to defend against a scare','Greatly get a bigger bonus on scaring people','Greatly Deal bonus damage to the Headless Horseman'][c[0]['bonus']] + '"',color=discord.Color.brand_green()).set_footer(text='This effect will last for one hour.')

      await interaction.response.send_message(embeds=[embed])

  @eat_candy.autocomplete('candy')
  async def eat_candy_autocomplete(self, interaction: discord.Interaction, current: str):
    try:
      if self.bot.ready == False:
        return

      if await self.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND guild_id = $2", interaction.user.id, interaction.guild_id) == None:
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

  async def cd_check(interaction: discord.Interaction) -> Optional[app_commands.Cooldown]:
    users = list(interaction.data['resolved']['users'].keys())
    user_raw = interaction.data['resolved']['users'][users[0]]
    user = interaction.guild.get_member(int(user_raw['id']))

    if await extra_functions.readyCheckCD(interaction.client, interaction) == False:
      return

    if int(user.id) == interaction.user.id:
      return
    elif user.bot == True:
      return

    target_data = await interaction.client.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", user.id, interaction.guild_id)

    if target_data == None or len(target_data['candy_bag']) < 10:
      return

    cds = await interaction.client.db_pool.fetchrow("SELECT * FROM command_cooldowns WHERE Guild_ID = $1", interaction.guild_id)

    return app_commands.Cooldown(1, cds['scare'] * 60)

  @app_commands.command(name="collect_vote_bonus",description='Collect either 50 candy or 10 golden candy from voting!')
  @app_commands.choices(bonus = [Choice(name="50 Regular Candy", value="0"), Choice(name="10 Golden Candy", value="1")])
  @app_commands.describe(bonus = 'The bonus you want to collect.')
  async def collectgoldenbonus(self, interaction: discord.Interaction, bonus: Choice[str]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Vote Candy Command Execute')
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
          return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW
      bonus = int(bonus.value)
      vote_data = await self.bot.vote_log.fetchrow('SELECT * FROM votes WHERE User_ID = $1', interaction.user.id)
      if vote_data == None and await extra_functions.getPremium(self.bot, interaction) == False:
        vote_check = False 
        try:
          vote_check = await self.bot.topggpy.get_user_info(int(interaction.user.id))
        except Exception as e:
          self.bot.logger.error('Vote Get Failed - ' + str(e))
        if vote_check == False:
          embed = discord.Embed(title='🔗   You need to vote first!   🔗',description='⠀\nYou need to vote first before you collect your daily box! Vote by pressing the button below.\n⠀',color=discord.Color.dark_gold()).set_footer(text='For any questions/concerns please visit the official TheKWitt server!')
          return await interaction.response.send_message(embeds=[embed], view=Links())

      user_data = await extra_functions.getUserData(self.bot, interaction.guild, interaction.user)
      
      if user_data['vote_cooldown'] > time.time():
        t = user_data['vote_cooldown'] - time.time()
        return await interaction.response.send_message("You\'ve used this command recently. Please wait " + str(int(t/60)) + " minutes, " + str(int(t+1) % 60) + " seconds!", ephemeral=True)

      if bonus == 0:
        candies = [ca for ca in self.bot.candy if ca['type'] != 'Golden']
        temp = []
        for x in range(50):
          candy = random.choice(candies)
          temp.append(int(candy['id']))
        await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag, $1), vote_cooldown = $4 WHERE member_id = $2 AND guild_id = $3', temp, interaction.user.id, interaction.guild_id, time.time() + 43200)
        embed = discord.Embed(title=interaction.user.name + ' got candy!', description='Thanks for the vote. You now have 50 more pieces of candy in your candy bag!',color=discord.Color.gold())
        return await interaction.response.send_message(embeds=[embed])
      elif bonus == 1:
        candies = [ca for ca in self.bot.candy if ca['type'] == 'Golden']
        temp = []
        for x in range(10):
          candy = random.choice(candies)
          temp.append(int(candy['id']))
        await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag, $1), vote_cooldown = $4 WHERE member_id = $2 AND guild_id = $3', temp, interaction.user.id, interaction.guild_id, time.time() + 43200)
        embed = discord.Embed(title=interaction.user.name + ' got golden candy!', description='Thanks for the vote. You now have 10 more golden pieces of candy in your candy bag!',color=discord.Color.gold())
        return await interaction.response.send_message(embeds=[embed])

  @app_commands.command(name="scare",description='Scare someone to try to take their candy!')
  @app_commands.describe(user='The user to scare')
  @app_commands.checks.dynamic_cooldown(cd_check, key=lambda i: (i.guild_id, i.user.id))
  async def scare(self, interaction: discord.Interaction, user: discord.User):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Scare Command Execute')
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
          return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      
      settings = await extra_functions.getGuildSettings(self.bot, interaction.guild)

      if settings['enable_scare'] == False:
        return await interaction.response.send_message(content='Scaring players is disabled.')
      
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW

      if await self.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", user.id, interaction.guild_id) == None:
          await extra_functions.Insert_User(self.bot,interaction.guild.id,user.id)   

      if user.id == interaction.user.id:
        return await interaction.response.send_message(content='You can\'t scare yourself!')
      elif user.bot == True:
        return await interaction.response.send_message(content='Bots are not intimidated by you.')

      user_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", interaction.user.id, interaction.guild_id)
      target_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", user.id, interaction.guild_id)

      if target_data == None or len(target_data['candy_bag']) < 10:
        return await interaction.response.send_message(content='This user has less than 10 pieces of candy in their candy bag. Choose another user to steal candy from.')
      
      settings = await extra_functions.getGuildSettings(self.bot, interaction.guild)
      chancePercent = 50
      scarePercent = settings['candy_steal_percent'] / 100

      if user_data['eat_bonus'] == 4:
        scarePercent = scarePercent * 1.5

      if user_data['eat_bonus'] == 10:
        scarePercent = scarePercent * 1.5

      if user_data['eat_bonus'] == 3:
        chancePercent = 80

      if user_data['eat_bonus'] == 9:
        chancePercent = 95

      description = 'Looks like ' + user.display_name + ' wasn\'t intimidated by their scare!'
      title = interaction.user.display_name + ' failed to scare ' + user.display_name + '!'
      percent = random.randint(0, 100)
      if percent > chancePercent:
        amount = int(scarePercent * len(target_data['candy_bag'])) + 1
        for x in range(amount):
          c = random.choice(list(target_data['candy_bag']))
          user_data['candy_bag'].append(c)
          target_data['candy_bag'].remove(c)

        percent2 = random.randint(0, 100)

        description = 'They stole ' + str(amount) + ' pieces of candy from the candy bag!'

        if target_data['eat_bonus'] == 2 and len(user_data['candy_bag']) > 0 and percent2 > 66:
          revenge = int(amount * 0.5) + 1
          for x in range(revenge):
            c = random.choice(list(user_data['candy_bag']))
            target_data['candy_bag'].append(c)
            user_data['candy_bag'].remove(c)

          description = 'They stole ' + str(amount) + ' pieces of candy from the candy bag! After adding it to their candy bag, they discovered some of their candy is missing as well! ' + user.display_name + ' got revenge and stole ' + str(revenge) + ' pieces of candy from them!'
        
        if target_data['eat_bonus'] == 8 and len(user_data['candy_bag']) > 0 and percent2 > 66:
          revenge = int(amount * 0.8) + 1
          for x in range(revenge):
            c = random.choice(list(user_data['candy_bag']))
            target_data['candy_bag'].append(c)
            user_data['candy_bag'].remove(c)

          description = 'They stole ' + str(amount) + ' pieces of candy from the candy bag! After adding it to their candy bag, they discovered some of their candy is missing as well! ' + user.display_name + ' got revenge and stole ' + str(revenge) + ' pieces of candy from them!'
        
        await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = $1 WHERE Member_ID = $2 and Guild_ID = $3;', user_data['candy_bag'], interaction.user.id, interaction.guild_id)
        await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = $1 WHERE Member_ID = $2 and Guild_ID = $3;', target_data['candy_bag'], user.id, interaction.guild_id)

        title = interaction.user.display_name + ' scared ' + user.display_name + '!'

      cds = await interaction.client.db_pool.fetchrow("SELECT * FROM command_cooldowns WHERE Guild_ID = $1", interaction.guild_id)
      embed = discord.Embed(title=title,description='⠀\n' + description + '\n⠀',color=discord.Color.purple()).set_footer(text='You\'ll have to wait ' + str(cds['scare']) + ' minutes before you can use this cooldown again.')

      await interaction.response.send_message(embeds=[embed])
  
  @scare.error
  async def scare_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
      return await interaction.response.send_message("You\'ve used this command recently. Please wait " + str(int(error.retry_after/60)) + " minutes, " + str(int(error.retry_after+1) % 60) + " seconds!", ephemeral=True)

  @app_commands.command(name="quick_guide",description='Quick Guide')
  async def view_settings(self, interaction: discord.Interaction):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='view_settings Command Execute')
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
          return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW

      embed = discord.Embed(title='Quick Guide')
      embed.add_field(name='Player Guide', value= 'Hello player! It looks like you\'re new here. Let\'s give you a quick tour. You can start out by talking like normal on any channel regularly. Eventually, an event will happen in that channel.\n\nOne of these events is going to be a candy drop. Simply press the correct prompt button. Now you have some candy, keep talking to collect more.\n\nAfter you have some candy your bag, use /candybag to see what you got. You can actually eat any of these pieces of candy and gain a bonus to help you get ahead of the competition.', inline=False)
      embed.add_field(name='Moderator Guide', value= 'Hey mod! Thank you so much for adding the bot to the server. Here\'s a quick start of how the optimize your experience.\n\nYou can control any of the functionalities of the bot using /settings. This will allow you to adjust anything to the size of your server. You can also control and disable a couple of commands that you find unnecessary.\n\nThere are also some tools that you can use to add candy, remove users, wipe your database, and more!\n\nThere\'s also some useful information on why certain permissions must be allowed to further transparency on how the bot works.', inline=False)
      embed.set_footer(text='See more with /help')

      await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(CandyCommands(bot))