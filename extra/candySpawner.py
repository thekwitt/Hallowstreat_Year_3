import time
import discord, random, asyncio
from discord.ext.tasks import loop
from discord import app_commands
from discord.ext import commands
from typing import List
from extra.discord_functions import extra_functions

class messageButton(discord.ui.Button['message_spawn']):
    def __init__(self, type: int, emoji, settings):

      super().__init__(style=discord.ButtonStyle.success, emoji=emoji, row=0)
      self._type = type
      self.settings = settings


    async def callback(self, interaction: discord.Interaction):
      assert self.view is not None
      view: message_spawn = self.view

      winss = ['The candy happily bounced out of the bunch and landed in your hand!', 'You stare deeply into the bag and grab the best looking piece of candy you could find.', 'You closed your eyes and grabbed the closest candy from the bunch.']
      loses = ['You picked up the candy but a crow flew by and grabbed it from you!', 'You grab and accidently dropped the candy and it exploded on the ground!', 'The candy ran away from you as soon as you grabbed it!', 'You fell face first while trying to pick up the candy.']
      stoles = ['You picked up the candy but a crow flew by and stole your candy while you weren\'t looking!', 'While trying to grab the candy, a spider lands on your hand and scares you! You lost some of your candy from the startle!', 'The candy in your bag got jealous and hopped out to find a new owner.', 'You fell face first while trying to pick up the candy and spilled some of your own!']
      types = ['Corn', 'Soda', 'Suckers', 'Swirls', 'Wraps', 'Chewy', 'Swag', 'Gummy', 'Banana', 'Gums', 'Jawbreakers']
             #['Swirls', 'Suckers', 'Banana', 'Wraps', 'Gums', 'Gummy', 'Swag', 'Soda', 'Jawbreakers', 'Chewy', 'Cane', 'Corn']
      candies = [ca for ca in view.bot.candy if ca['type'] != 'Golden']


      await extra_functions.beforeCommand(view.bot, interaction)

      user_data = await view.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND Guild_id = $2", interaction.user.id, interaction.guild_id)

      if(view.type < 10):
        candies = [candy for candy in view.bot.candy if candy['type'] == types[view.type]]

      if interaction.user.id in view.people and view.people[interaction.user.id][1] == True:
        try:
          return await interaction.response.send_message('You already tried to grab candy! Wait until the next bunch.', ephemeral=True)
        except:
          view.bot.logger.error(str(interaction.guild.id) + ' | ' + str(interaction.user.id) + ' - Candy Message Send Fail')

      if self._type == 1:
        change_if_fucked = False
        if interaction.user.id in view.people and view.people[interaction.user.id][1] == False:
          change_if_fucked = True
        view.people[interaction.user.id] = [0, True]
        view.win.append(interaction.user.name)
        view.bot.logger.info(extra_functions.printGuildUserDetails(interaction.guild, interaction.user) + ' - Candy Message Grabbed')

        wins = 0
        for p in view.people:
          if view.people[p][0] == 0:
            wins += 1

        if self.settings['candy_object_per_drop'] <= wins:
          view.finished = True
          await extra_functions.reloadMessageDrop(bot=view.bot, guild=interaction.guild)
          view.stop()
          for child in view.children:
            if child._type == 1:
              child.style = discord.ButtonStyle.success
            elif child._type == 2:
              child.style = discord.ButtonStyle.danger
            child.disabled = True
          embed = discord.Embed(title='Everyone took from the bunch!',description='⠀\nKeep on talking for another one to appear!\n⠀⠀',color= discord.Color.dark_gold()).set_footer(text='Each bunch only lasts ' + str(self.settings['drop_duration']) + ' seconds!').set_image(url='')
          if len(view.win) != 0:
            embed.add_field(name='Picked the Correct Candy', value = ' '.join(view.win))

          if len(view.lose) != 0:
            embed.add_field(name='Picked the Wrong Candy', value = ' '.join(view.lose))

          try:
            await interaction.response.edit_message(embeds= [embed], view=view)
          except:
            view.bot.logger.error(str(interaction.guild.id) + ' | ' + str(interaction.user.id) + ' - Candy Message Game Over Edit Fail')
            return await extra_functions.reloadMessageDrop(bot=view.bot, guild=interaction.guild)

        amount = self.settings['candy_obtain_amount']
        if user_data['eat_bonus'] == 0:
          amount = int(amount * 1.5)
        elif user_data['eat_bonus'] == 1 and change_if_fucked == False:
          amount = int(amount * 1.15)
        elif user_data['eat_bonus'] == 7 and change_if_fucked == False:
          amount = int(amount * 1.3)          
        elif user_data['eat_bonus'] == 6:
          amount = int(amount * 2)
        elif user_data['eat_bonus'] == 1 and change_if_fucked == True:
          amount = int(amount * 0.75)
        elif user_data['eat_bonus'] == 7 and change_if_fucked == True:
          amount = int(amount * 1)

        candy_won = random.choices(candies, k=amount)
        candy_string = ''
        candy_inv = []
        candy_pre = []
        for c in candy_won:
          candy_pre.append(c['emoji'])
          candy_inv.append(int(c['id']))
        candy_string = ' '.join(candy_pre)
        await view.bot.db_pool.execute('UPDATE user_data SET candy_completion = uniq(sort(array_cat(candy_completion,$1))), candy_bag = array_cat(candy_bag,$1), candy_collected = candy_collected + $2 WHERE Member_ID = $3 and Guild_ID = $4;', candy_inv, len(candy_inv), interaction.user.id, interaction.guild_id)
        win_string = random.choice(winss)
        embed = discord.Embed(title='Awesome! You got some candy!',description='⠀\n' + win_string + '\nSee what candy you won below!\n⠀⠀', color=discord.Color.blurple())
        embed.set_footer(text='Make sure to pay attention on the next bunch!')
        embed.set_image(url='')
        embed.add_field(name='Candy Won',value= candy_string)
        try:
          if view.finished == True:
            await interaction.followup.send(embeds= [embed], ephemeral=True)
          else:
            await interaction.response.send_message(embeds= [embed], ephemeral=True)
        except:
          view.bot.logger.error(str(interaction.guild.id) + ' | ' + str(interaction.user.id) + ' - Candy Message Em Message Send Fail')

      elif self._type == 2:
        if user_data['eat_bonus'] == 1 or user_data['eat_bonus'] == 7:
          view.people[interaction.user.id] = [1, False]
        else:
          view.people[interaction.user.id] = [1, True]

        view.lose.append(interaction.user.name)
        view.bot.logger.info(extra_functions.printGuildUserDetails(interaction.guild, interaction.user) + ' - Candy Message Missed')
        try:
          loss_string = '⠀\n' + random.choice(loses) + '\n⠀'
          if user_data['eat_bonus'] == 1:
            loss_string = '⠀\nLuckily you ate a piece of candy that gives you a second change to get the bunch! If you manage to guess it correctly the second time, you\'ll get slightly less than normal candy.\n⠀'
          if user_data['eat_bonus'] == 7:
            loss_string = '⠀\nLuckily you ate a piece of candy that gives you a second change to get the bunch! If you manage to guess it correctly the second time, you\'ll get the exact amount of candy you would get the first time.\n⠀'
          embed = discord.Embed(title='Oh no you choose wrong!',description=loss_string, color=discord.Color.dark_purple()).set_footer(text='Make sure to pay attention on the next bunch!')
          embed.set_image(url='')
          if view.finished == True:
            await interaction.followup.send(embeds= [embed], ephemeral=True)
          else:
            await interaction.response.send_message(embeds= [embed], ephemeral=True)
        except:
          view.bot.logger.error(str(interaction.guild.id) + ' | ' + str(interaction.user.id) + ' - Candy Message Send Fail')


      #await interaction.response.edit_message(embed=, view=view)

class message_spawn(discord.ui.View):
  children: List[messageButton]

  def __init__(self, timeout, bot, pick, settings, type):
    super().__init__(timeout=timeout)
    self.people = {}
    self.win = []
    self.lose = []
    self.finished = False
    self.bot = bot
    self.type = type
    self.settings = settings
    winner = random.randint(0, 2)
    types = ['Banana', 'Soda', 'Wraps', 'Jawbreakers', 'Corn']

    for x in range(3):
      if(x == winner):
        temp = random.choice([candy for candy in bot.candy if candy['type'] == types[pick]])['emoji']
        self.add_item(messageButton(1, temp, settings))
      else:
        temp = random.choice([candy for candy in bot.candy if candy['type'] != types[pick] and candy['type'] != 'Golden'])['emoji']
        self.add_item(messageButton(2, temp, settings))
    
  async def on_timeout(self):
    if self.finished == False:
      for child in self.children:
        if child._type == 1:
          child.style = discord.ButtonStyle.success
        elif child._type == 2:
          child.style = discord.ButtonStyle.danger
        child.disabled = True

      await extra_functions.reloadMessageDrop(bot=self.bot, guild=self.response.guild)

      try: 
        embed = discord.Embed(title='The remaining candy vanished!',description='⠀\nKeep on talking for another one to appear!\n⠀',color=discord.Color.dark_orange()).set_footer(text='Each bunch only lasts ' + str(self.settings['drop_duration']) + ' seconds!').set_image(url='')
        
        if len(self.win) != 0:
          embed.add_field(name='Picked the Correct Candy', value = ' '.join(self.win))

        if len(self.lose) != 0:
          embed.add_field(name='Picked the Wrong Candy', value = ' '.join(self.lose))
        
        await self.response.edit(embeds= [embed], view=self)
      except:
        self.bot.logger.error(str(self.response.guild.id) + ' - Expired Message Fail Edit')
        return await extra_functions.reloadMessageDrop(bot=self.bot, guild=self.response.guild)

class SpawnCandy:
  async def spawnCandy(self, message):
    try:
      self.bot.messages[str(message.guild.id)]['activeMessage'] = True
      settings = await extra_functions.getGuildSettings(self.bot, message.guild)
      percent = random.randint(0, 20)          
      title = 'A Bunch of Candy suddenly appeared!'
      image = 'https://cdn.discordapp.com/attachments/782835367085998080/896615714251747378/bunch_o_candy.png'
      type = 11
      if percent < 10:
        rand = random.randint(0, 10)
        titles = ['A Bunch of Candy Corn suddenly appeared!', 'A Bunch of Soda suddenly appeared!', 'A Bunch of Suckers suddenly appeared!', 'A Bunch of Swirls suddenly appeared!', 'A Bunch of Wraps suddenly appeared!', 'A Bunch of Chewys suddenly appeared!', 'A Bunch of Swag Bars suddenly appeared!', 'A Bunch of Gummies suddenly appeared!', 'A Bunch of Bananas suddenly appeared!', 'A Bunch of Gum suddenly appeared!', 'A Bunch of Jawbreakers suddenly appeared!']
        images = ['https://cdn.discordapp.com/attachments/782835367085998080/894418632929583184/bunch_o_suckers.png', 'https://media.discordapp.net/attachments/889230894693482519/900589348448251934/bunch_o_soda.png', 'https://cdn.discordapp.com/attachments/782835367085998080/894418632929583184/bunch_o_suckers.png', 'https://cdn.discordapp.com/attachments/782835367085998080/894418629699993610/bunch_o_spirals.png', 'https://cdn.discordapp.com/attachments/782835367085998080/896495134529687602/bunch_o_wraps.png', 'https://media.discordapp.net/attachments/889230894693482519/900589347189981194/bunch_o_chews.png', 'https://media.discordapp.net/attachments/889230894693482519/900589346372071444/bunch_o_swag.png', 'https://media.discordapp.net/attachments/889230894693482519/900589344274907206/bunch_o_gummy.png', 'https://media.discordapp.net/attachments/889230894693482519/900589342622371890/bunch_o_bananas.png', 'https://media.discordapp.net/attachments/782835367085998080/896615718894841926/bunch_o_gum.png', 'https://media.discordapp.net/attachments/782835367085998080/896615776214200340/bunch_o_jawbreakers.png']
        type = rand
        title = titles[rand]
        image = images[rand]
      names = ['Hard Banana', 'Hard Soda', 'Wrapped Candy', 'Circular Jawbreaker', 'Candy Corn']
      pick = random.randint(0, 4)

      try:
        view = message_spawn(timeout=settings['drop_duration'], bot=self.bot, pick=pick, type=type, settings=settings)
        embed = discord.Embed(title=title,description='⠀\nLook at all this candy! Press the **' + names[pick] + '** button to get it!\n⠀', color=discord.Color.orange()).set_footer(text='You can only get one at a time!')
        embed.set_image(url=image)
        channel = message.guild.get_channel(random.choice(settings['channel_id']))
        m = await channel.send(embeds= [embed], view=view)
        view.response = m
        self.bot.logger.info(extra_functions.printGuildDetails(message.guild) + ' - Candy Message Sent')
      except Exception as e:
        self.bot.logger.error(extra_functions.printGuildDetails(message.guild) + ' - Candy Message Send Fail | ' + str(e))
        return await extra_functions.reloadMessageDrop(bot=self.bot, guild=message.guild)
    except:
      return await extra_functions.reloadMessageDrop(bot=self.bot, guild=message.guild)

  async def spawnCandyVC(bot, guild):
    try:
      bot.messages[str(guild.id)]['activeMessage'] = True
      settings = await extra_functions.getGuildSettings(bot, guild)
      percent = random.randint(0, 20)          
      title = 'A Bunch of Candy suddenly appeared!'
      image = 'https://cdn.discordapp.com/attachments/782835367085998080/896615714251747378/bunch_o_candy.png'
      type = 11
      if percent < 10:
        rand = random.randint(0, 10)
        titles = ['A Bunch of Candy Corn suddenly appeared!', 'A Bunch of Soda suddenly appeared!', 'A Bunch of Suckers suddenly appeared!', 'A Bunch of Swirls suddenly appeared!', 'A Bunch of Wraps suddenly appeared!', 'A Bunch of Chewys suddenly appeared!', 'A Bunch of Swag Bars suddenly appeared!', 'A Bunch of Gummies suddenly appeared!', 'A Bunch of Bananas suddenly appeared!', 'A Bunch of Gum suddenly appeared!', 'A Bunch of Jawbreakers suddenly appeared!']
        images = ['https://cdn.discordapp.com/attachments/782835367085998080/894418632929583184/bunch_o_suckers.png', 'https://media.discordapp.net/attachments/889230894693482519/900589348448251934/bunch_o_soda.png', 'https://cdn.discordapp.com/attachments/782835367085998080/894418632929583184/bunch_o_suckers.png', 'https://cdn.discordapp.com/attachments/782835367085998080/894418629699993610/bunch_o_spirals.png', 'https://cdn.discordapp.com/attachments/782835367085998080/896495134529687602/bunch_o_wraps.png', 'https://media.discordapp.net/attachments/889230894693482519/900589347189981194/bunch_o_chews.png', 'https://media.discordapp.net/attachments/889230894693482519/900589346372071444/bunch_o_swag.png', 'https://media.discordapp.net/attachments/889230894693482519/900589344274907206/bunch_o_gummy.png', 'https://media.discordapp.net/attachments/889230894693482519/900589342622371890/bunch_o_bananas.png', 'https://media.discordapp.net/attachments/782835367085998080/896615718894841926/bunch_o_gum.png', 'https://media.discordapp.net/attachments/782835367085998080/896615776214200340/bunch_o_jawbreakers.png']
        type = rand
        title = titles[rand]
        image = images[rand]
      names = ['Hard Banana', 'Hard Soda', 'Wrapped Candy', 'Circular Jawbreaker', 'Candy Corn']
      pick = random.randint(0, 4)

      try:
        view = message_spawn(timeout=settings['drop_duration'], bot=bot, pick=pick, type=type, settings=settings)
        embed = discord.Embed(title=title,description='⠀\nLook at all this candy! Press the **' + names[pick] + '** button to get it!\n⠀', color=discord.Color.orange()).set_footer(text='You can only get one at a time!')
        embed.set_image(url=image)
        channel = guild.get_channel(random.choice(settings['channel_id']))
        m = await channel.send(embeds= [embed], view=view)
        view.response = m
        bot.logger.info(extra_functions.printGuildDetails(guild) + ' - Candy Message Sent')
      except Exception as e:
        bot.logger.error(extra_functions.printGuildDetails(guild) + ' - Candy Message Send Fail | ' + str(e))
        return await extra_functions.reloadMessageDrop(bot=bot, guild=guild)
    except:
      return await extra_functions.reloadMessageDrop(bot=bot, guild=guild)

  async def spawnCandyInteraction(self, interaction):
    try:
      self.bot.messages[str(interaction.guild_id)]['activeMessage'] = True
      settings = await extra_functions.getGuildSettings(self.bot, interaction.guild)

      percent = random.randint(0, 21)          
      title = 'A Bunch of Candy suddenly appeared!'
      image = 'https://cdn.discordapp.com/attachments/782835367085998080/896615714251747378/bunch_o_candy.png'
      type = 11
      if percent < 10:
        rand = random.randint(0, 10)
        titles = ['A Bunch of Candy Corn suddenly appeared!', 'A Bunch of Soda suddenly appeared!', 'A Bunch of Suckers suddenly appeared!', 'A Bunch of Swirls suddenly appeared!', 'A Bunch of Wraps suddenly appeared!', 'A Bunch of Chemys suddenly appeared!', 'A Bunch of Swag Bars suddenly appeared!', 'A Bunch of Gummies suddenly appeared!', 'A Bunch of Bananas suddenly appeared!', 'A Bunch of Gum suddenly appeared!', 'A Bunch of Jawbreakers suddenly appeared!']
        images = ['https://cdn.discordapp.com/attachments/782835367085998080/894418632929583184/bunch_o_suckers.png', 'https://media.discordapp.net/attachments/889230894693482519/900589348448251934/bunch_o_soda.png', 'https://cdn.discordapp.com/attachments/782835367085998080/894418632929583184/bunch_o_suckers.png', 'https://cdn.discordapp.com/attachments/782835367085998080/894418629699993610/bunch_o_spirals.png', 'https://cdn.discordapp.com/attachments/782835367085998080/896495134529687602/bunch_o_wraps.png', 'https://media.discordapp.net/attachments/889230894693482519/900589347189981194/bunch_o_chews.png', 'https://media.discordapp.net/attachments/889230894693482519/900589346372071444/bunch_o_swag.png', 'https://media.discordapp.net/attachments/889230894693482519/900589344274907206/bunch_o_gummy.png', 'https://media.discordapp.net/attachments/889230894693482519/900589342622371890/bunch_o_bananas.png', 'https://media.discordapp.net/attachments/782835367085998080/896615718894841926/bunch_o_gum.png', 'https://media.discordapp.net/attachments/782835367085998080/896615776214200340/bunch_o_jawbreakers.png']
        type = rand
        title = titles[rand]
        image = images[rand]
      names = ['Hard Banana', 'Hard Soda', 'Wrapped Candy', 'Circular Jawbreaker', 'Candy Corn']
      pick = random.randint(0, 4)

      view = message_spawn(timeout=settings['drop_duration'], bot=self.bot, pick=pick, type=type, settings=settings)
      try:
        embed = discord.Embed(title=title,description='⠀\nLook at all this candy! Press the **' + names[pick] + '** button to get it!\n⠀', color=discord.Color.orange()).set_footer(text='You can only get one at a time!')
        embed.set_image(url=image)
        channel = interaction.guild.get_channel(random.choice(settings['channel_id']))
        m = await channel.send(embeds= [embed], view=view)
        view.response = m
        self.bot.logger.info(extra_functions.printGuildDetails(interaction.guild) + ' - Candy Message Sent')
      except Exception as e:
        self.bot.logger.error(extra_functions.printGuildDetails(interaction.guild) + ' - Candy Message Send Fail | ' + str(e))
        return await extra_functions.reloadMessageDrop(bot=self.bot, guild=interaction.guild)
    except:
      return await extra_functions.reloadMessageDrop(bot=self.bot, guild=interaction.guild)
