from itertools import count
from urllib import response
import discord, math, time, random, psutil, os
from discord import app_commands, Interaction
from discord.ext import commands
from discord.app_commands import AppCommandError
from extra.discord_functions import extra_functions
from extra.candySpawner import SpawnCandy
from extra.bossSpawnerHard import SpawnBoss

class Links2(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Support Server', url='https://discord.com/invite/ZNpCNyNubU'))

class ModTools(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name='bot_holter',description='See how the bot is performing right now!')
  async def ping(self, interaction:discord.Interaction):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='spawn candy Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
      # DO CODE BELOW

      embed = discord.Embed(title='The Holter', color=discord.Color.brand_red())

      embed.add_field(name = 'Discord Latency', value=f'`{round(interaction.client.latency * 1000)}ms`')
      embed.add_field(name= 'Bot Latency', value=f'`{round((time.time() - interaction.created_at.timestamp()) * 1000)}ms`')
      embed.add_field(name='\u200B', value='\u200B',inline=False)
      embed.add_field(name='Total Servers', value= f'`{len(interaction.client.guilds):,}`')
      count = 0
      for g in interaction.client.guilds:
        count += g.member_count      
      embed.add_field(name='Total Users', value= f'`{count:,}`')
      embed.add_field(name='Total Shards', value= f'`{interaction.client.shard_count:,}`')
      embed.add_field(name='\u200B', value='\u200B',inline=False)
      process = psutil.Process(os.getpid())
      embed.add_field(name='CPU Usage', value= f'`{round(process.cpu_percent(),2)} %`')
      embed.add_field(name='Ram Usage', value= f'`{round(process.memory_percent(),2)} %`')

      await interaction.response.send_message(embed=embed)



  @app_commands.command(name="spawn_candy_drop",description='Skip the timer and spawn a candy drop!')
  async def spawn_candy_drop(self, interaction: discord.Interaction):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='spawn candy Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      if await extra_functions.returnPremiumMessage(self.bot, interaction) == False:
        return

      # DO CODE BELOW
      if not str(interaction.guild.id) in list(self.bot.messages.keys()):
        await extra_functions.reloadMessageDrop(bot=self.bot, guild=interaction.guild)


      messageSpawn = self.bot.messages[str(interaction.guild.id)]

      if messageSpawn == None:
        try:
          await interaction.response.send_message(content='Looks like your server wasn\'t listed for candy yet! Talk for a minute for the bot to register it.')
        except:
          extra_functions.logUseError(self.bot, interaction.user, interaction.guild, 'Candy Spawn Command Drop Already Fail Send')


      if messageSpawn['activeMessage'] == False:
        try:
          try:
            await interaction.response.send_message(content='Confirmed! The Candy Drop has spawned!')
          except:
            extra_functions.logUseError(self.bot, interaction.user, interaction.guild, 'Candy Spawn Command Drop Already Fail Send')

          await SpawnCandy.spawnCandyInteraction(self, interaction)
        except:
          return
      elif messageSpawn['activeMessage'] == True:
        try:
          await interaction.response.send_message(content='The drop has already spawned!')
        except:
          extra_functions.logUseError(self.bot, interaction.user, interaction.guild, 'Candy Spawn Command Drop Already Fail Send')

  @app_commands.command(name="spawn_headless_horseman",description='Skip the timer and spawn a boss!')
  async def spawn_headless_horseman(self, interaction: discord.Interaction):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='spawn boss Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      if await extra_functions.returnPremiumMessage(self.bot, interaction) == False:
        return

      # DO CODE BELOW
      if not str(interaction.guild.id) in list(self.bot.messages.keys()):
        await extra_functions.reloadMessageDrop(bot=self.bot, guild=interaction.guild)


      messageSpawn = self.bot.messages[str(interaction.guild.id)]

      if messageSpawn == None:
        try:
          await interaction.response.send_message(content='Looks like your server wasn\'t listed for candy or bosses yet! Talk for a minute for the bot to register it.')
        except:
          extra_functions.logUseError(self.bot, interaction.user, interaction.guild, 'Boss Spawn Command Drop Already Fail Send')


      if messageSpawn['activeMessage'] == False:
        try:
          try:
            await interaction.response.send_message(content='Confirmed! The Boss has spawned!')
          except:
            extra_functions.logUseError(self.bot, interaction.user, interaction.guild, 'Boss Spawn Command Drop Already Fail Send')

          await SpawnBoss.spawnBossInteraction(self, interaction)
        except:
          return
      elif messageSpawn['activeMessage'] == True:
        try:
          await interaction.response.send_message(content='The drop has already spawned!')
        except:
          extra_functions.logUseError(self.bot, interaction.user, interaction.guild, 'Boss Spawn Command Drop Already Fail Send')


  @commands.Cog.listener()
  async def on_app_command_completion(self, interaction: discord.Interaction, command: app_commands.Command) -> bool:
    if self.bot.ready == False:
      return

    try:
        await extra_functions.change_roles(self.bot, interaction.guild)
    except Exception as e:
        self.bot.logger.error(str(interaction.guild.id) + ' | Change Role Fail: ' + str(e))


    user_data = await extra_functions.getUserData(self.bot, interaction.guild, interaction.user)

    if user_data == None:
      return

    if user_data['first_time'] == False:
      try:
        embed = discord.Embed(title='Quick Guide', color=discord.Color.blue())
        embed.add_field(name='Player Guide', value= 'Hello player! It looks like you\'re new here. Let\'s give you a quick tour. You can start out by talking like normal on any channel regularly. Eventually, an event will happen in that channel.\n\nOne of these events is going to be a candy drop. Simply press the correct prompt button. Now you have some candy, keep talking to collect more.\n\nAfter you have some candy your bag, use /candybag to see what you got. You can actually eat any of these pieces of candy and gain a bonus to help you get ahead of the competition.', inline=False)
        embed.add_field(name='Moderator Guide', value= 'Hey mod! Thank you so much for adding the bot to the server. Here\'s a quick start of how the optimize your experience.\n\nYou can control any of the functionalities of the bot using /settings. This will allow you to adjust anything to the size of your server. You can also control and disable a couple of commands that you find unnecessary.\n\nThere are also some tools that you can use to add candy, remove users, wipe your database, and more!\n\nThere\'s also some useful information on why certain permissions must be allowed to further transparency on how the bot works.', inline=False)
        embed.set_footer(text='See more with /help')
        try:
          await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
          await interaction.followup.send(embed=embed, ephemeral=True)
        await self.bot.db_pool.execute('UPDATE user_data SET first_time = TRUE WHERE Guild_ID = $1 AND Member_ID = $2;', interaction.guild_id, interaction.user.id)
      except:
        extra_functions.logUseError(self.bot, interaction.user, interaction.guild_id, 'No send first time')
    elif user_data['bot_update'] == False:
      try:
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        every_data = await self.bot.db_pool.fetch('SELECT * FROM user_data WHERE bot_update = TRUE;')
        description = 'Hello! Bot Master TheKWitt here!\n\nThe Thanksgiving bot is now live for beta inviting! Invite it on your server now!\n\nAlso this bot will be offline at <t:1667880000:f>. Have seven extra days for being so awesome!\n\nSee you then and thank you everyone for using this bot! Let this be a great start to the 3rd Year of Seasonal Bots!'
        embed = discord.Embed(title='Bot Update',description= '⠀\n' + description + '\n⠀', color=discord.Color.brand_red())
        embed.set_footer(text='You are the ' + str(ordinal(len(every_data) + 1)) + ' person to view this update!')
        try:
          await interaction.response.send_message(embed=embed, view=Links2(), ephemeral=True)
        except:
          await interaction.followup.send(embed=embed, view=Links2(), ephemeral=True)
        await self.bot.db_pool.execute('UPDATE user_data SET bot_update = TRUE WHERE Guild_ID = $1 AND Member_ID = $2;', interaction.guild_id, interaction.user.id)
      except:
        extra_functions.logUseError(self.bot, interaction.user, interaction.guild_id, 'No bot update')
    elif user_data['eat_notify'] == True:
      try:
        try:
          await interaction.response.send_message(content='Your bonus has expired! Eat another candy to resume it.', ephemeral=True)
        except:
          await interaction.followup.send(content='Your bonus has expired! Eat another candy to resume it.', ephemeral=True)
        await self.bot.db_pool.execute('UPDATE user_data SET eat_notify = FALSE WHERE Guild_ID = $1 AND Member_ID = $2',  interaction.guild_id, interaction.user.id)
      except:
        extra_functions.logUseError(self.bot, interaction.user, interaction.guild_id, 'No send bonus expire')

  @app_commands.command(name="add_channel_spawn",description='Add another channel to the possible channels that can spawn.')
  @app_commands.describe(channel='The channel you want candy to spawn in.')
  async def add_channel_spawn(self, interaction: discord.Interaction, channel: discord.TextChannel):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='add_channel_spawn Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      settings = await extra_functions.getGuildSettings(self.bot, interaction.guild)
      if channel.id in settings['channel_id']:
        return await interaction.response.send_message(content='This channel already exists in the list!')

      if len(settings['channel_id']) >= 5:
        return await interaction.response.send_message(content='You already have 5 channels, remove one first.')
        
      await self.bot.db_pool.execute('UPDATE guild_settings SET Channel_ID = array_append(Channel_ID, $2) WHERE guild_id = $1', interaction.guild_id, channel.id)
      await interaction.response.send_message('The channel has been added.')

  @app_commands.command(name="remove_channel_spawn",description='Add another channel to the possible channels that can spawn.')
  @app_commands.describe(channel='The channel you want candy to spawn in.')
  async def remove_channel_spawn(self, interaction: discord.Interaction, channel: discord.TextChannel):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='remove_channel_spawn Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      settings = await extra_functions.getGuildSettings(self.bot, interaction.guild)
     
      if len(settings['channel_id']) == 1:
        return await interaction.response.send_message(content='You cannot have less than one channel.')
     
      if not channel.id in settings['channel_id']:
        return await interaction.response.send_message(content='This channel does not exist in the list!')
        
      await self.bot.db_pool.execute('UPDATE guild_settings SET Channel_ID = array_remove(Channel_ID, $2) WHERE guild_id = $1', interaction.guild_id, channel.id)
      await interaction.response.send_message('The channel has been removed.')


  @app_commands.command(name="setup",description='Setup the bot for your server.')
  @app_commands.describe(channel='The channel you want candy to spawn in.')
  async def setup(self, interaction: discord.Interaction, channel: discord.TextChannel):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='setup Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      if not 'hallow\'s champion' in [r.name.lower() for r in interaction.guild.roles]:
        try:
          await interaction.guild.create_role(name="Hallow\'s Champion", color= discord.Color.orange())
        except:
          return await interaction.response.send_message(content='Looks like your bot doesn\'t have manage role perms. Please make sure that **View Channel, Send Messages, Embed Links, and Use External Emoji** Permissions are ticked in the role and/or channel')
        
      await self.bot.db_pool.execute('UPDATE guild_settings SET setup = TRUE, Channel_ID = $2 WHERE guild_id = $1', interaction.guild_id, [channel.id])
      await interaction.response.send_message('The bot has now been setup! Here are some things to keep in mind.\n\nThe bot needs **View Channel, Send Messages, Embed Links, and Use External Emoji** Permissions to be ticked in the role that the bot has and/or channel that you just have setup.\n\nMessage spawns will occur after a certain time has passed and message have been sent on the server (That the bot can view with View_Settings Permissions). You can check these with **/settings view_settings** and **/drop_clock**.\n\nIf you are still confused, please refer to the **/help** command or use **/support** to get direct help from TheKWitt himself. Cheers!')

  @app_commands.command(name="erase_member",description='Erase a member from your server\'s database. (CANNOT UNDO)')
  @app_commands.describe(user='The player you want to remove.')
  async def erasemember(self, interaction: discord.Interaction, user: discord.User):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Erase Member Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('DELETE from user_data WHERE Guild_ID = $2 AND Member_ID = $1;', user.id, interaction.guild.id)
      await interaction.response.send_message(user.mention + ' has been removed. This action cannot be undone.')

  @app_commands.command(name="erase_members",description='Erase members with a certain role from your server\'s database. (CANNOT UNDO)')
  @app_commands.describe(role='The Role of People you want to remove.')
  async def erasemembers(self, interaction: discord.Interaction, role: discord.Role):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Erase Members Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW

      if len(role.members) == 0:
        await interaction.response.send_message(ephemeral= True, content= 'Looks like this role has no one in it! Try another one!')
      
      await self.bot.db_pool.execute('DELETE from user_data WHERE Guild_ID = $2 AND Member_ID = ANY($1);', [member.id for member in role.members], interaction.guild.id)
      await interaction.response.send_message('Users with ' + role.mention + ' have been removed. This action cannot be undone.')

  @app_commands.command(name="erase_guild",description='Erase a server\'s database. (CANNOT UNDO)')
  async def eraseguild(self, interaction: discord.Interaction):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Erase Guild Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW
      
      await self.bot.db_pool.execute('DELETE from user_data WHERE Guild_ID = $1;', interaction.guild.id)
      await interaction.response.send_message('Server has been removed. This action cannot be undone.')

  @app_commands.command(name="drop_clock",description='See when the next drop will spawn.')
  async def dropclock(self, interaction: discord.Interaction):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Drop Clock Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW

      if not str(interaction.guild.id) in list(self.bot.messages.keys()):
        await extra_functions.reloadMessageDrop(bot=self.bot, guild=interaction.guild)

      messageSpawn = self.bot.messages[str(interaction.guild.id)]
      
      strings = ['None!', 'None!']

      if(messageSpawn['timestamp'] - time.time()) > 0:
        strings[0] = '' + str(math.floor(messageSpawn['timestamp'] - time.time())) + ' Seconds'

      if(messageSpawn.get('messageCount') - 1 > 0):
        strings[1] = '' + str(messageSpawn['messageCount'])

      embed = discord.Embed(title='🕒   The Drop Clock   🕒')
      embed.set_footer(text='If you don\'t like these settings, you can always change them with the /settings command!')
      embed.add_field(name='Time Remaining', value=strings[0], inline=False)
      embed.add_field(name='Messages Remaining', value=strings[1], inline=False)

      await interaction.response.send_message(embed=embed)

  @app_commands.command(name="reload_drop",description='Is the drop stuck? Reload with this command.')
  async def reloaddrop(self, interaction: discord.Interaction):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Reload Drop Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW

      await extra_functions.reloadMessageDrop(self.bot, interaction.guild)
      await interaction.response.send_message('The drop has been reloaded.')

  @app_commands.command(name="add_candy_user",description='Add candy to a single user.')
  @app_commands.describe(user='The player you want to add candy to.', amount = 'Amount of candy you want to add.')
  async def addcandyuser(self, interaction: discord.Interaction, user: discord.User, amount: app_commands.Range[int, 1, 100]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='addcandyuser Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW

      if await self.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", user.id, interaction.guild_id) == None:
          await extra_functions.Insert_User(self.bot, interaction.guild.id, user.id)

      candies = self.bot.candy
      candy_won = random.choices(candies, k=amount)
      candy_pre = []
      for c in candy_won:
        candy_pre.append(int(c['id']))
      
      await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag,$1) WHERE Member_ID = $2 and Guild_ID = $3;', candy_pre,  user.id, interaction.guild_id)
      await interaction.response.send_message(user.mention + ' now has ' + str(amount) + ' more pieces of candy.')

  @app_commands.command(name="add_candy_role",description='Add candy to all users of a role.')
  @app_commands.describe(role='Add candy to users of a role', amount = 'Amount of candy you want to add.')
  async def addcandyrole(self, interaction: discord.Interaction, role: discord.Role, amount: app_commands.Range[int, 1, 100]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='addcandyrole Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      if len(role.members) == 0:
        await interaction.response.send_message(ephemeral= True, content= 'Looks like this role has no one in it! Try another one!')

      # DO CODE BELOW

      if await extra_functions.returnPremiumMessage(self.bot, interaction) == False:
        return

      candies = [c for c in self.bot.candy if c['type'] != 'Golden']
      candy_won = random.choices(candies, k=amount)
      candy_pre = []
      for c in candy_won:
        candy_pre.append(int(c['id']))

      ids = [member.id for member in role.members]
      
      await self.bot.db_pool.execute('INSERT INTO user_data (Guild_ID, Member_ID) VALUES ($1, UNNEST($2::bigint[])) ON CONFLICT DO NOTHING;', interaction.guild_id, ids)
      await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag, $1) WHERE Guild_ID = $3 AND Member_ID = ANY($2);', candy_pre, ids, interaction.guild_id)
      await interaction.response.send_message('Users with ' + role.mention + ' have been granted candy.')

  @app_commands.command(name="remove_candy_user",description='Remove candy to a single user.')
  @app_commands.describe(user='The player you want to remove candy from.', amount = 'Amount of candy you want to remove.')
  async def removecandyuser(self, interaction: discord.Interaction, user: discord.User, amount: app_commands.Range[int, 1, 5000]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='addcandyuser Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
        return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)

      if interaction.user.guild_permissions.manage_channels == False:
        return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

      # DO CODE BELOW

      if await self.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", user.id, interaction.guild_id) == None:
          await extra_functions.Insert_User(self.bot, interaction.guild.id, user.id)

      user_data = await extra_functions.getUserData(self.bot, interaction.guild, user)

      if len(user_data['candy_bag']) < amount:
        amount = len(user_data['candy_bag'])

      for c in range(amount):
        user_data['candy_bag'].pop()
      
      await self.bot.db_pool.execute('UPDATE user_data SET candy_bag = $1 WHERE Member_ID = $2 and Guild_ID = $3;', user_data['candy_bag'],  user.id, interaction.guild_id)
      await interaction.response.send_message(user.mention + ' now has ' + str(len(user_data['candy_bag'])) + ' pieces of candy.')

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(ModTools(bot))