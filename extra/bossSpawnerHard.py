import math
import time, json
from unicodedata import name
import discord, random, asyncio
from discord.ext.tasks import loop
from discord import app_commands
from discord.ext import commands
from typing import List
from extra.discord_functions import extra_functions

class FireView(discord.ui.View):
  def __init__(self, parent, settings):
    self.fires = [False,False,False]
    self.parent = parent
    super().__init__(timeout=None)

  @discord.ui.button(emoji='🔥', style=discord.ButtonStyle.red, custom_id='1')
  async def fire1(self, interaction: discord.Interaction, button: discord.ui.Button):
    assert self.parent is not None
    view: message_spawn = self.parent
    self.fires[0] = True
    button.disabled = True
    if all(self.fires) == True:
      if view.fireSolve[0] != 0:
        self.parent.fireSolve = [interaction.user.id, True]
        await interaction.response.send_message(content='You put out all the fires!', ephemeral=True)
      else:
        await interaction.response.send_message(content='You helped someone put out all the fires!', ephemeral=True)
      self.stop()
    else:
      await interaction.response.edit_message(view=self)

  @discord.ui.button(emoji='🔥', style=discord.ButtonStyle.red, custom_id='2')
  async def fire2(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.fires[1] = True
    button.disabled = True
    if all(self.fires) == True:
      if self.parent.fireSolve[0] != 0:
        self.parent.fireSolve = [interaction.user.id, True]
        await interaction.response.send_message(content='You put out all the fires!', ephemeral=True)
      else:
        await interaction.response.send_message(content='You helped someone put out all the fires!', ephemeral=True)
      self.stop()
    else:
      await interaction.response.edit_message(view=self)

  @discord.ui.button(emoji='🔥', style=discord.ButtonStyle.red, custom_id='3')
  async def fire3(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.fires[2] = True
    button.disabled = True
    if all(self.fires) == True:
      if self.parent.fireSolve[0] != 0:
        self.parent.fireSolve = [interaction.user.id, True]
        await interaction.response.send_message(content='You put out all the fires!', ephemeral=True)
      else:
        await interaction.response.send_message(content='You helped someone put out all the fires!', ephemeral=True)
      self.stop()
    else:
      await interaction.response.edit_message(view=self)

async def rewardGrant(bot, guild, people):
  list_people = list(people)
  if len(people) >= 3:
    temp_candy = []
    for x in range(3):
      c = [ca for ca in bot.candy if ca['type'] == 'Golden']
      temp_candy.append(int(random.choice(c)['id']))
    
    for x in range(25):
      c = [ca for ca in bot.candy if ca['type'] != 'Golden']
      temp_candy.append(int(random.choice(c)['id']))
      
    await bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag, $1), candy_completion = uniq(sort(array_cat(candy_completion,$1))) WHERE guild_id = $2 AND member_id = $3', temp_candy, guild.id, list_people[0])
    
    temp_candy = []
    for x in range(2):
      c = [ca for ca in bot.candy if ca['type'] == 'Golden']
      temp_candy.append(int(random.choice(c)['id']))

    for x in range(15):
      c = [ca for ca in bot.candy if ca['type'] != 'Golden']
      temp_candy.append(int(random.choice(c)['id']))
     
    await bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag, $1), candy_completion = uniq(sort(array_cat(candy_completion,$1))) WHERE guild_id = $2 AND member_id = $3', temp_candy, guild.id, list_people[1])

    temp_candy = []
    c = [ca for ca in bot.candy if ca['type'] == 'Golden']
    temp_candy.append(int(random.choice(c)['id']))
    for x in range(10):
      c = [ca for ca in bot.candy if ca['type'] != 'Golden']
      temp_candy.append(int(random.choice(c)['id']))
    await bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag, $1), candy_completion = uniq(sort(array_cat(candy_completion,$1))) WHERE guild_id = $2 AND member_id = ANY($3)', temp_candy, guild.id, list_people[2:])

  if len(people) == 2:
    temp_candy = []
    for x in range(3):
      c = [ca for ca in bot.candy if ca['type'] == 'Golden']
      temp_candy.append(int(random.choice(c)['id']))

    for x in range(25):
      c = [ca for ca in bot.candy if ca['type'] != 'Golden']
      temp_candy.append(int(random.choice(c)['id']))
      
    await bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag, $1), candy_completion = uniq(sort(array_cat(candy_completion,$1))) WHERE guild_id = $2 AND member_id = $3', temp_candy, guild.id, list_people[0])
    
    temp_candy = []
    for x in range(2):
      c = [ca for ca in bot.candy if ca['type'] == 'Golden']
      temp_candy.append(int(random.choice(c)['id']))

    for x in range(15):
      c = [ca for ca in bot.candy if ca['type'] != 'Golden']
      temp_candy.append(int(random.choice(c)['id']))
      
    await bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag, $1), candy_completion = uniq(sort(array_cat(candy_completion,$1))) WHERE guild_id = $2 AND member_id = $3', temp_candy, guild.id, list_people[1])
  
  if len(people) == 1:
    temp_candy = []
    for x in range(3):
      c = [ca for ca in bot.candy if ca['type'] == 'Golden']
      temp_candy.append(int(random.choice(c)['id']))

    for x in range(25):
      c = [ca for ca in bot.candy if ca['type'] != 'Golden']
      temp_candy.append(int(random.choice(c)['id']))
      
    await bot.db_pool.execute('UPDATE user_data SET candy_bag = array_cat(candy_bag, $1), candy_completion = uniq(sort(array_cat(candy_completion,$1))) WHERE guild_id = $2 AND member_id = $3', temp_candy, guild.id, list_people[0])

def is_what_percent_of(num_a, num_b):
    return (num_a / num_b) * 100

def clock_calc(time_left, time_max):
  percent = is_what_percent_of(time_left, time_max)
  clocks = ['🕐','🕑','🕒','🕓','🕔','🕕','🕖','🕗','🕘','🕙','🕚','🕛']
  for x in range(12):
    require = 100 - (((x+1)/12) * 100)
    if require <= percent:
      return(clocks[x])
  return '🕛'

def health_calc(damage, health, paramaters):
  total = 100 - math.floor((damage/health) * 100)
  string = ''
  if total < paramaters[1]:
    para_total = is_what_percent_of(total, paramaters[1])
    for x in range(10):
      if x * 10 >= para_total:
        string += '🟥'
      else:
        string += '🟧'
  elif total < paramaters[0]:
    para_total = is_what_percent_of(total - paramaters[1], paramaters[0] - paramaters[1])
    for x in range(10):
      if x * 10 >= para_total:
        string += '🟧'
      else:
        string += '🟨'
  else:
    para_total = is_what_percent_of(total - paramaters[0], 100 - paramaters[0])
    for x in range(10):
      if x * 10 >= para_total:
        string += '🟨'
      else:
        string += '🟩'
  return string

def calc_damage(users, damage):
  return (damage / users) * 1.05

class messageButton(discord.ui.Button['message_spawn']):
    def __init__(self, type: int, style, content, settings):

      super().__init__(style=style, label = content, row=0)
      self._type = type
      self.settings = settings


    async def callback(self, interaction: discord.Interaction):
      assert self.view is not None
      view: message_spawn = self.view

      await extra_functions.beforeCommand(view.bot, interaction)
      
      if await view.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", interaction.user.id, interaction.guild_id) == None:
          await extra_functions.Insert_User(view.bot,interaction.guild.id,interaction.user.id)   

      user_data = await view.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND Guild_id = $2", interaction.user.id, interaction.guild_id)

      if self._type == 0: # Tutorial
        await interaction.response.send_message('Hey Player! This is battle event. You must work together in order to defeat the Headless Horseman.\n\nAll you have to do is follow what the prompts tell you do. You\'ll be Dealing Damage, Dodging and Countering attacks and Extinguishing Fire!\n\nGood Luck!', ephemeral=True)
      if self._type == 1: # Ambush
        if not interaction.user.id in view.peopleMissCount:
          view.peopleMissCount[interaction.user.id] = 0
        view.peopleRecent[interaction.user.id] = 5
        if not interaction.user.id in view.peopleAmbush:
          if user_data['eat_bonus'] == 5:
            view.peopleAmbush[interaction.user.id] = 1.1
            await interaction.response.send_message(content='Excellent! You successfully ambushed the bot with your **Power Up** bonus before the battle began!\n\nYou can only ambush once so wait for the battle to begin to start plowing some sick damage!', ephemeral=True)
          elif user_data['eat_bonus'] == 11:
            view.peopleAmbush[interaction.user.id] = 1.2
            await interaction.response.send_message(content='Excellent! You successfully ambushed the bot with your **Super Power Up** before the battle began!\n\nYou can only ambush once so wait for the battle to begin to start plowing some sick damage!', ephemeral=True)
          else:
            view.peopleAmbush[interaction.user.id] = 1
            await interaction.response.send_message(content='Excellent! You successfully ambushed the bot before the battle began!\n\nYou can only ambush once so wait for the battle to begin to start plowing some sick damage!', ephemeral=True)     
        else:
          await interaction.response.send_message(content='You already ambushed! Please wait for the battle to begin.', ephemeral=True)
      elif self._type == 2: # Hit

        if interaction.user.id in view.peopleStun:
          await interaction.response.send_message(content='You are stunned!\nYou have to wait ' + str(view.peopleStun[interaction.user.id]) + ' seconds before you can attack again.', ephemeral=True)
        else:
          await interaction.response.defer()
        view.peopleRecent[interaction.user.id] = 5
        if not interaction.user.id in view.peopleMissCount:
          view.peopleMissCount[interaction.user.id] = 0

        if user_data['eat_bonus'] == 5:
          dam = calc_damage(len(view.peopleRecent),1.1)
          if not interaction.user.id in view.peopleDamage:
            view.peopleDamage[interaction.user.id] = dam
          else:
            view.peopleDamage[interaction.user.id] += dam
          view.damage += dam
        elif user_data['eat_bonus'] == 11:
          dam = calc_damage(len(view.peopleRecent),1.2)
          if not interaction.user.id in view.peopleDamage:
            view.peopleDamage[interaction.user.id] = dam
          else:
            view.peopleDamage[interaction.user.id] += dam
          view.damage += dam
        else:
          dam = calc_damage(len(view.peopleRecent),1.0)
          if not interaction.user.id in view.peopleDamage:
            view.peopleDamage[interaction.user.id] = dam
          else:
            view.peopleDamage[interaction.user.id] += dam
          view.damage += dam
      elif self._type == 3: # Miss Stun
        view.peopleRecent[interaction.user.id] = 5
        if not interaction.user.id in view.peopleMissCount:
          view.peopleMissCount[interaction.user.id] = 1
        else:
          view.peopleMissCount[interaction.user.id] += 1
        if not interaction.user.id in view.peopleStun:
          view.peopleStun[interaction.user.id] = 5
          await interaction.response.send_message(content='You missed an attack and the headless horse man stunned you!\nYou must wait 5 seconds before you can attack again.', ephemeral=True)
        else:
          await interaction.response.send_message(content='You are stunned!\nYou have to wait ' + str(view.peopleStun[interaction.user.id]) + ' seconds before you can attack again.', ephemeral=True)
      elif self._type == 4: # Miss Heal
        if not interaction.user.id in view.peopleMissCount:
          view.peopleMissCount[interaction.user.id] = 1
        else:
          view.peopleMissCount[interaction.user.id] += 1
        view.peopleRecent[interaction.user.id] = 5
        if view.phaseHealth[1] > ((view.health - view.damage) / view.health) * 100:
          view.damage -= calc_damage(len(view.peopleRecent),[0.3,0.6,1,1.2][self.settings['boss_difficulty']])
          await interaction.response.send_message(content='You missed an attack and that allowed the headless horseman to absorb some of your life essense! Healing him for alittle!', ephemeral=True)
      elif self._type == 5: # Dodge
        view.peopleRecent[interaction.user.id] = 5
        if not interaction.user.id in view.peopleDodge or view.peopleDodge[interaction.user.id] == None:
          view.peopleDodge[interaction.user.id] = True
          await interaction.response.send_message(content='You successfully got ready to dodge the attack! You will not be stunned after the brief period.\nPlease wait to start attacking again', ephemeral=True)
        elif view.peopleDodge[interaction.user.id] != None:
          await interaction.response.send_message(content='You already tried to dodge!\nPlease wait to start attacking again.', ephemeral=True)
      elif self._type == 6: # Miss Dodge

        view.peopleRecent[interaction.user.id] = 5
        if not interaction.user.id in view.peopleMissCount:
          view.peopleMissCount[interaction.user.id] = 1
        else:
          view.peopleMissCount[interaction.user.id] += 1
        if not interaction.user.id in view.peopleDodge or view.peopleDodge[interaction.user.id] == None:
          view.peopleDodge[interaction.user.id] = False
          await interaction.response.send_message(content='You tripped which has left you open to be attacked! You will be stunned after the brief period.\nPlease wait to start attacking again', ephemeral=True)
        elif view.peopleDodge[interaction.user.id] != None:
          await interaction.response.send_message(content='You already tried to dodge!\nPlease wait to start attacking again.', ephemeral=True)
      elif self._type == 7: # Counter
        view.peopleRecent[interaction.user.id] = 5
        if not interaction.user.id in view.peopleMissCount:
          view.peopleMissCount[interaction.user.id] = 0
        if not interaction.user.id in view.peopleDodge or view.peopleDodge[interaction.user.id] == None:
          view.peopleDodge[interaction.user.id] = True
          await interaction.response.send_message(content='You successfully got ready to counter the attack! You will not be stunned and will deal damage to the boss after the brief period.\nPlease wait to start attacking again', ephemeral=True)
        elif view.peopleDodge[interaction.user.id] != None:
          await interaction.response.send_message(content='You already tried to counter!\nPlease wait to start attacking again.', ephemeral=True)
      elif self._type == 8: # Miss Counter
        if not interaction.user.id in view.peopleMissCount:
          view.peopleMissCount[interaction.user.id] = 1
        else:
          view.peopleMissCount[interaction.user.id] += 1
        view.peopleRecent[interaction.user.id] = 5
        if not interaction.user.id in view.peopleDodge or view.peopleDodge[interaction.user.id] == None:
          view.peopleDodge[interaction.user.id] = False
          await interaction.response.send_message(content='You tripped which has left you open to be attacked! You will be stunned after the brief period.\nPlease wait to start attacking again', ephemeral=True)
        elif view.peopleDodge[interaction.user.id] != None:
          await interaction.response.send_message(content='You already tried to dodge!\nPlease wait to start attacking again.', ephemeral=True)
      elif self._type == 9: # Fire Solve
        view.peopleRecent[interaction.user.id] = 5
        view.fireSolve -= 1
        await interaction.response.defer()
      #await interaction.response.edit_message(embed=, view=view)

class message_spawn(discord.ui.View):
  children: List[messageButton]

  def __init__(self, bot, descriptions, settings, guild):
    super().__init__(timeout=None)
    self.guild = guild
    self.peopleDamage = {}
    self.peopleRecent = {}
    self.peopleAmbush = {}
    self.peopleDodge = {}
    self.peopleStun = {}
    self.peopleMissCount = {}
    self.peopleHeal = {}
    self.fireSolve = 0
    self.bot = bot
    self.phase = 0
    self.phaseHealth = [70, 25]
    self.damage = 0
    self.finished = False
    self.health = [60,75,90,105][settings['boss_difficulty']]
    self.dodgeCount = 0
    self.settings = settings
    self.cooldown = 6
    self.pictures = []
    self.swap = random.randint(5,8)
    self.countToChange = 0
    self.countToObsticle = 0
    self.timeLeft = 130
    self.descriptions = descriptions
    self.images = ['https://cdn.discordapp.com/attachments/782835367085998080/1028735159320719441/Phase_1.png','https://cdn.discordapp.com/attachments/782835367085998080/1028735160432214046/Prephase_2.png','https://cdn.discordapp.com/attachments/782835367085998080/1028735159639474297/Phase_2.png','https://cdn.discordapp.com/attachments/782835367085998080/1028727045150220378/Prephase_3.png','https://cdn.discordapp.com/attachments/782835367085998080/1028727044701433956/Phase_3.png','https://cdn.discordapp.com/attachments/782835367085998080/1027379140082532372/fire.png','','']

    self.add_item(messageButton(type = 0, style=discord.ButtonStyle.gray, content='Tutorial', settings=self.settings))
    self.checker.start()

  @loop(seconds=1)
  async def checker(self):

    if self.finished == True:
      return

    if self.timeLeft <= 0:
      return await self.on_timeout()

    if self.phase == 1: # Build Up Phase
      self.clear_items()
      self.add_item(messageButton(type = 0, style=discord.ButtonStyle.gray, content='Tutorial', settings=self.settings))
      self.add_item(messageButton(type = 1, style=discord.ButtonStyle.red, content='Ambush', settings=self.settings))
      embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + self.descriptions['intro'][1] + '\n⠀', color=discord.Color.purple()).set_footer(text='Get ready for an intense battle')
      embed.set_image(url=self.images[0])
      embed.set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
      self.phase = 2
      try:
        await self.response.edit(embed=embed, view=self)
      except Exception as e:
        self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 1 | ' + str(e))

    elif self.phase == 2: # Setup for Phase 1
      if self.countToObsticle > 7:
        if len(self.peopleRecent) != 0:
          self.damage = math.floor(self.health * 0.05)
          dam = calc_damage(len(self.peopleRecent),math.floor(self.health * 0.05))
          for person in list(self.peopleRecent):
            self.peopleDamage[person] = dam

        self.countToObsticle = 0
        self.phase = 3
        embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle1']) + '\n⠀', color=discord.Color.orange())
        embed.set_image(url=self.images[0])
        embed.set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
        battle_embed = discord.Embed(title='Action Belt',description='⠀\nPress the **Hit** Button as fast as you can to deal damage!\n⠀', color=discord.Color.brand_red()).set_footer(text='Next Button Swap is in ' + str(self.swap) + ' seconds\n(Hint: 5 clicks per 5 seconds before it tells you to slow down!)')
        battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
        battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
        self.countToObsticle = 0
        hit = random.randint(0,2)
        self.clear_items()

        for x in range(3):
          if(x == hit):
            self.add_item(messageButton(type = 2, style=discord.ButtonStyle.red, content='Hit!', settings=self.settings))
          else:
            self.add_item(messageButton(type = 3, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
        try:
          await self.response.edit(embeds=[embed,battle_embed], view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 2 | ' + str(e))
        self.swap = random.randint(5,8)
      self.countToObsticle += 1
    elif self.phase == 3: # Phase 1
      if self.dodgeCount == 0:
        self.timeLeft -= 1
      
      # Check timeouts
      for person in list(self.peopleStun):
        self.peopleStun[person] -= 1
        if self.peopleStun[person] <= 0:
          del self.peopleStun[person]

      for person in list(self.peopleRecent):
        self.peopleRecent[person] -= 1
        if self.peopleRecent[person] <= 0:
          del self.peopleRecent[person]

      if 100 - math.floor((self.damage/self.health) * 100) < self.phaseHealth[0]: # Switch to Phase 2 Intro
        self.phase = 4
        self.countToChange = 0
        self.countToObsticle = 0
        self.dodgeCount = 0
        self.countToChange = 0
        self.peopleDodge = {}
        self.clear_items()
        embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + self.descriptions['phase2'][0] + '\n⠀', color=discord.Color.purple())
        embed.set_image(url=self.images[1])
        try:
          await self.response.edit(embed=embed, view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 3 | ' + str(e))


      # Check Obsticle
      elif self.countToChange >= self.cooldown:
        if self.countToObsticle < 3:
          self.countToChange = 0
          embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle1']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
          embed.set_image(url=self.images[0])
          
          battle_embed = discord.Embed(title='Action Belt',description='⠀\nPress the **Hit** Button as fast as you can to deal damage!\n⠀', color=discord.Color.brand_red()).set_footer(text='Next Button Swap is in ' + str(self.swap) + ' seconds\n(Hint: 5 clicks per 5 seconds before it tells you to slow down!)')
          battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
          battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
          hit = random.randint(0,2)
          self.clear_items()
          for x in range(3):
            if(x == hit):
              self.add_item(messageButton(type = 2, style=discord.ButtonStyle.red, content='Hit!', settings=self.settings))
            else:
              self.add_item(messageButton(type = 3, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
          
          try:
            await self.response.edit(embeds=[embed,battle_embed], view=self)
          except Exception as e:
            self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 4 | ' + str(e))
          self.swap = random.randint(5,8)
        else:
          if self.dodgeCount == 0:
            for person in list(self.peopleRecent):
              self.peopleDodge[person] = None
            self.swap = random.randint(5,8)
            embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle1']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
            embed.set_image(url=self.images[0])
            
            battle_embed = discord.Embed(title='Action Belt',description='⠀\nThe Headless horseman is charging at you!\n**Press the Dodge Button to evade the attack!**\n⠀', color=discord.Color.brand_red()).set_footer(text='You have five seconds to evade the attack!')
            battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
            battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
            hit = random.randint(0,2)
            self.clear_items()
            for x in range(3):
              if(x == hit):
                self.add_item(messageButton(type = 5, style=discord.ButtonStyle.green, content='Dodge!', settings=self.settings))
              else:
                self.add_item(messageButton(type = 6, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
            try:
              await self.response.edit(embeds=[embed,battle_embed], view=self)
            except Exception as e:
              self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 5 | ' + str(e))
            self.dodgeCount += 1
          elif self.dodgeCount < 5:
            self.dodgeCount += 1
          elif self.dodgeCount >= 5:
            temp_win = []
            temp_lose = []
            names_win = []
            names_lose = []

            for person in list(self.peopleDodge):
              member = self.guild.get_member(person)
              if self.peopleDodge[person] == False or self.peopleDodge[person] == None:
                names_lose.append(member.name)
                temp_lose.append(person)
              elif self.peopleDodge[person] == True:
                names_win.append(member.name)
                temp_win.append(person)

            for temp in temp_lose:
              self.peopleStun[temp] = 5

            string_win = ', '.join(names_win)
            string_lose = ', '.join(names_lose)

            self.countToObsticle = 0
            self.dodgeCount = 0
            self.countToChange = 0
            self.peopleDodge = {}
            embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle1']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
            embed.set_image(url=self.images[0])
            
            if string_lose != '':
              string_lose = string_lose + ' got hit by the attack and got stunned five seconds!\n'
            if string_win != '':
              string_win += ' managed to dodge the attack!\n'

            string_split = ''
            if string_lose != '' or string_win != '':
              string_split = '\n'

            battle_embed = discord.Embed(title='Action Belt',description='⠀\n' + string_win + string_lose + string_split + 'Press the **Hit** Button as fast as you can to deal damage!\n⠀', color=discord.Color.brand_red()).set_footer(text='Next Button Swap is in ' + str(self.swap) + ' seconds\n(Hint: 5 clicks per 5 seconds before it tells you to slow down!)')
            battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
            battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
            hit = random.randint(0,2)
            self.clear_items()
            for x in range(3):
              if(x == hit):
                self.add_item(messageButton(type = 2, style=discord.ButtonStyle.red, content='Hit!', settings=self.settings))
              else:
                self.add_item(messageButton(type = 3, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
            
            try:
              await self.response.edit(embeds=[embed,battle_embed], view=self)
            except Exception as e:
              self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 6 | ' + str(e))
        # Increment Obsticle
        self.countToObsticle += 1
      self.countToChange += 1
    elif self.phase == 4: # Setup for Phase 2
      if self.countToObsticle == 4:
        embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + self.descriptions['phase2'][1] + '\n⠀', color=discord.Color.purple())
        embed.set_image(url=self.images[2])
        embed.set_footer(text='Get ready for the next phase!')
        try:
          await self.response.edit(embed=embed, view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 7 | ' + str(e))
        self.swap = random.randint(5,8)
      elif self.countToObsticle == 9:
        self.phase = 5
        embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle2']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
        embed.set_image(url=self.images[2])
        
        battle_embed = discord.Embed(title='Action Belt',description='⠀\nPress the **Hit** Button as fast as you can to deal damage!\n⠀', color=discord.Color.brand_red()).set_footer(text='Next Button Swap is in ' + str(self.swap) + ' seconds\n(Hint: 5 clicks per 5 seconds before it tells you to slow down!)')
        battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
        battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
        self.countToObsticle = 0
        hit = random.randint(0,3)
        self.clear_items()

        for x in range(4):
          if(x == hit):
            self.add_item(messageButton(type = 2, style=discord.ButtonStyle.red, content='Hit!', settings=self.settings))
          else:
            self.add_item(messageButton(type = 3, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
        
        try:
          await self.response.edit(embeds=[embed,battle_embed], view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 8 | ' + str(e))
        self.swap = random.randint(5,8)
      self.countToObsticle += 1
    elif self.phase == 5: # Phase 2  
      if self.dodgeCount == 0:
        self.timeLeft -= 1
      
      # Check timeouts
      for person in list(self.peopleStun):
        self.peopleStun[person] -= 1
        if self.peopleStun[person] <= 0:
          del self.peopleStun[person]

      for person in list(self.peopleRecent):
        self.peopleRecent[person] -= 1
        if self.peopleRecent[person] <= 0:
          del self.peopleRecent[person]

      if 100 - math.floor((self.damage/self.health) * 100) < self.phaseHealth[1]: # Switch to Phase 3 Intro
        self.phase = 6
        self.countToChange = 0
        self.countToObsticle = 0
        self.dodgeCount = 0
        self.countToChange = 0
        self.peopleDodge = {}
        self.clear_items()
        embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + self.descriptions['phase3'][0] + '\n⠀', color=discord.Color.purple())
        embed.set_image(url=self.images[3])
        try:
          await self.response.edit(embed=embed, view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 9 | ' + str(e))

      # Check Obsticle
      elif self.countToChange >= self.cooldown:
        if self.countToObsticle < 2:
          self.countToChange = 0
          embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle2']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
          embed.set_image(url=self.images[2])
          
          battle_embed = discord.Embed(title='Action Belt',description='⠀\nPress the **Hit** Button as fast as you can to deal damage!\n⠀', color=discord.Color.brand_red()).set_footer(text='Next Button Swap is in ' + str(self.swap) + ' seconds\n(Hint: 5 clicks per 5 seconds before it tells you to slow down!)')
          battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
          battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
          hit = random.randint(0,3)
          self.clear_items()
          for x in range(4):
            if(x == hit):
              self.add_item(messageButton(type = 2, style=discord.ButtonStyle.red, content='Hit!', settings=self.settings))
            else:
              self.add_item(messageButton(type = 3, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
          
          try:
            await self.response.edit(embeds=[embed,battle_embed], view=self)
          except Exception as e:
            self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 10| ' + str(e))
          self.swap = random.randint(5,8)
        else:
          if self.dodgeCount == 0:
            for person in list(self.peopleRecent):
              self.peopleDodge[person] = None
            self.swap = random.randint(5,8)
            embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle2']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
            embed.set_image(url=self.images[2])
            
            battle_embed = discord.Embed(title='Action Belt',description='⠀\nThe Headless horseman is charging at you!\n**Press the Dodge Button to evade the attack!**\n⠀', color=discord.Color.brand_red()).set_footer(text='You have five seconds to evade the attack!')
            battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
            battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
            hit = random.randint(0,3)
            self.clear_items()
            for x in range(4):
              if(x == hit):
                self.add_item(messageButton(type = 7, style=discord.ButtonStyle.blurple, content='Counter!', settings=self.settings))
              else:
                self.add_item(messageButton(type = 8, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
            try:
              await self.response.edit(embeds=[embed,battle_embed], view=self)
            except Exception as e:
              self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 11 | ' + str(e))
            self.dodgeCount += 1
          elif self.dodgeCount < 5:
            self.dodgeCount += 1
          elif self.dodgeCount >= 5:
            temp_win = []
            temp_lose = []
            names_win = []
            names_lose = []

            for person in list(self.peopleDodge):
              member = self.guild.get_member(person)
              if self.peopleDodge[person] == False or self.peopleDodge[person] == None:
                names_lose.append(member.name)
                temp_lose.append(person)
              elif self.peopleDodge[person] == True:
                names_win.append(member.name)
                temp_win.append(person)

            if len([p for p in self.peopleDodge if self.peopleDodge[p] == True]) != 0:
              self.damage += math.floor(self.health * 0.03)
              dam = calc_damage(len(self.peopleDodge),math.floor(self.health * 0.03))
              for person in list(self.peopleDodge):
                if not person in self.peopleDamage:
                  self.peopleDamage[person] = dam
                else:
                  self.peopleDamage[person] += dam

            for temp in temp_lose:
              self.peopleStun[temp] = 5

            string_win = ', '.join(names_win)
            string_lose = ', '.join(names_lose)

            self.countToObsticle = 0
            self.dodgeCount = 0
            self.countToChange = 0
            self.peopleDodge = {}
            if 100 - math.floor((self.damage/self.health) * 100) >= self.phaseHealth[1]: # Switch to Phase 3 Intro
              embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle2']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
              embed.set_image(url=self.images[2])
              
              if string_lose != '':
                string_lose = string_lose + ' got hit by the attack and got stunned five seconds!\n'
              if string_win != '':
                string_win += ' countered the attack and dealed damage!\n'

              string_split = ''
              if string_lose != '' or string_win != '':
                string_split = '\n'

              battle_embed = discord.Embed(title='Action Belt',description='⠀\n' + string_win + string_lose + string_split + 'Press the **Hit** Button as fast as you can to deal damage!\n⠀', color=discord.Color.brand_red()).set_footer(text='Next Button Swap is in ' + str(self.swap) + ' seconds\n(Hint: 5 clicks per 5 seconds before it tells you to slow down!)')
              battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
              battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
              hit = random.randint(0,2)
              self.clear_items()
              for x in range(3):
                if(x == hit):
                  self.add_item(messageButton(type = 2, style=discord.ButtonStyle.red, content='Hit!', settings=self.settings))
                else:
                  self.add_item(messageButton(type = 3, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
              
              try:
                await self.response.edit(embeds=[embed,battle_embed], view=self)
              except Exception as e:
                self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 12 | ' + str(e))
        # Increment Obsticle
        self.countToObsticle += 1
      self.countToChange += 1      
    elif self.phase == 6: # Setup for Phase 3
      if self.countToObsticle == 4:
        embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + self.descriptions['phase3'][1] + '\n⠀', color=discord.Color.purple())
        embed.set_image(url=self.images[4])
        embed.set_footer(text='Get ready for the next phase!')
        try:
          await self.response.edit(embed=embed, view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 13 | ' + str(e))
        self.swap = random.randint(5,8)
      elif self.countToObsticle == 9:
        self.phase = 7
        embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle3']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
        embed.set_image(url=self.images[4])
        
        battle_embed = discord.Embed(title='Action Belt',description='⠀\nPress the **Hit** Button as fast as you can to deal damage!\n⠀', color=discord.Color.brand_red()).set_footer(text='Next Button Swap is in ' + str(self.swap) + ' seconds\n(Hint: 5 clicks per 5 seconds before it tells you to slow down!)')
        battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
        battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
        self.countToObsticle = 0
        hit = random.randint(0,4)
        self.clear_items()

        for x in range(5):
          if(x == hit):
            self.add_item(messageButton(type = 2, style=discord.ButtonStyle.red, content='Hit!', settings=self.settings))
          else:
            self.add_item(messageButton(type = 3, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
        
        try:
          await self.response.edit(embeds=[embed,battle_embed], view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 14 | ' + str(e))
        self.swap = random.randint(5,8)
      self.countToObsticle += 1
    elif self.phase == 7: # Phase 3  
      self.timeLeft -= 1
      
      # Check timeouts
      for person in list(self.peopleStun):
        self.peopleStun[person] -= 1
        if self.peopleStun[person] <= 0:
          del self.peopleStun[person]

      for person in list(self.peopleRecent):
        self.peopleRecent[person] -= 1
        if self.peopleRecent[person] <= 0:
          del self.peopleRecent[person]
      if 100 - math.floor((self.damage/self.health) * 100) <= 0 and self.finished == False: # Swap to Ending
        self.phase = 8
        self.countToChange = 0
        self.countToObsticle = 0
        self.dodgeCount = 0
        self.countToChange = 0
        self.peopleDodge = {}
        self.clear_items()
        embed = discord.Embed(title='The Headless Horseman has been defeated!',description='⠀\n' + self.descriptions['death'][0] + '\n⠀', color=discord.Color.purple())
        embed.set_image(url=self.images[5])
        try:
          await self.response.edit(embed=embed, view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 15 | ' + str(e))

      # Check Obsticle
      elif self.countToChange >= self.cooldown:
        if self.countToObsticle < 3:
          self.countToChange = 0
          embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle3']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
          embed.set_image(url=self.images[4])
          
          battle_embed = discord.Embed(title='Action Belt',description='⠀\nPress the **Hit** Button as fast as you can to deal damage!\n⠀', color=discord.Color.brand_red()).set_footer(text='Next Button Swap is in ' + str(self.swap) + ' seconds\n(Hint: 5 clicks per 5 seconds before it tells you to slow down!)')
          battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
          battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
          hit = random.randint(0,4)
          self.clear_items()
          for x in range(5):
            if(x == hit):
              self.add_item(messageButton(type = 2, style=discord.ButtonStyle.red, content='Hit!', settings=self.settings))
            else:
              self.add_item(messageButton(type = 4, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
          
          try:
            await self.response.edit(embeds=[embed,battle_embed], view=self)
          except Exception as e:
            self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 16 | ' + str(e))
          self.swap = random.randint(5,8)
        else:
          if self.dodgeCount == 0:
            self.dodgeCount = 1
            self.fireSolve = len(self.peopleRecent) * 3 + 1
            self.swap = random.randint(5,8)
            embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle3']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
            embed.set_image(url=self.images[5])
            
            battle_embed = discord.Embed(title='Action Belt',description='⠀\nThe Headless horseman spread a ring of fire!\n**Press the Extingush Button as many times as you can to put out the fire!**\n⠀', color=discord.Color.brand_red()).set_footer(text='You cannot continue until someone puts the fire out!')
            battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
            battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
            self.clear_items()
            self.add_item(messageButton(type = 9, style=discord.ButtonStyle.red, content='Extingush!', settings=self.settings))
            try:
              await self.response.edit(embeds=[embed,battle_embed], view=self)
            except Exception as e:
              self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 17 | ' + str(e))
          elif self.fireSolve <= 0:
            self.countToObsticle = 0
            self.dodgeCount = 0
            self.countToChange = 0
            self.fireSolve = 0

            embed = discord.Embed(title='The Headless Horseman',description='⠀\n' + random.choice(self.descriptions['battle3']) + '\n⠀', color=discord.Color.orange()).set_footer(text= str(len(self.peopleRecent)) + ' players are currently battling!')
            embed.set_image(url=self.images[4])
            

            battle_embed = discord.Embed(title='Action Belt',description='⠀\nThe fire was put out!\n\nPress the **Hit** Button as fast as you can to deal damage!\n⠀', color=discord.Color.brand_red()).set_footer(text='Next Button Swap is in ' + str(self.swap) + ' seconds\n(Hint: 5 clicks per 5 seconds before it tells you to slow down!)')
            battle_embed.add_field(name = 'Health', value=health_calc(self.damage, self.health, self.phaseHealth))
            battle_embed.add_field(name = 'Time', value = clock_calc(self.timeLeft,120))
            hit = random.randint(0,4)
            self.clear_items()
            for x in range(5):
              if(x == hit):
                self.add_item(messageButton(type = 2, style=discord.ButtonStyle.red, content='Hit!', settings=self.settings))
              else:
                self.add_item(messageButton(type = 4, style=discord.ButtonStyle.grey, content='Miss!', settings=self.settings))
            
            try:
              await self.response.edit(embeds=[embed,battle_embed], view=self)
            except Exception as e:
              self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 18 | ' + str(e))
        # Increment Obsticle
        self.countToObsticle += 1
      self.countToChange += 1    
    elif self.phase == 8: # Ending
      if self.countToObsticle == 4:
        embed = discord.Embed(title='The Headless Horseman has been defeated!',description='⠀\n' + self.descriptions['death'][1] + '\n⠀', color=discord.Color.purple())
        embed.set_image(url=self.images[5])
        try:
          await self.response.edit(embed=embed, view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 19 | ' + str(e))
      if self.countToObsticle == 9:
        end_string = '```css\n[Rank] | {.Dmg / Miss.} | Treater\n==========================================\n'
        sorted_damage = dict(sorted(self.peopleDamage.items(), key=lambda item: item[1], reverse=True))
        i = 0
        for person in sorted_damage:

          try:
            sorted_damage[person]
          except (IndexError, KeyError, TypeError):
            break
          
          name = self.guild.get_member(person).display_name
          if i == 10:
            break
          end_string += " " + "[" + str(i+1).zfill(2) + "]" + "  |   " + str(math.floor(sorted_damage[person])).zfill(3) + " / " + str(self.peopleMissCount[person]).zfill(2) + "     | " + name[:13] + "\n"
          i += 1

        end_string += '```'
        rank_string = 'Rank 1 gets **3 Golden and 25 Regular Candy**\nRank 2 gets **2 Golden and 15 Regular Candy**\nRank 3 and Below gets **1 Golden and 10 Regular Candy**'

        if len(sorted_damage) == 2:
          rank_string = 'Rank 1 gets **3 Golden and 25 Regular Candy**\nRank 2 gets **2 Golden and 15 Regular Candy**'
        elif len(sorted_damage) == 1:
          rank_string = 'Rank 1 gets **3 Golden and 25 Regular Candy**'

        await rewardGrant(self.bot, self.guild, sorted_damage)
          
        embed = discord.Embed(title='The Battle has been Won!',description='⠀\n' + rank_string + '\n⠀', color=discord.Color.blurple())
        embed.set_image(url=self.images[5])
        embed.set_footer(text='Enjoy the glory!')

        logembed = discord.Embed(title='Battle Results',description='⠀\n' + end_string +'\n⠀', color=discord.Color.greyple())
        try:
          await self.response.edit(embeds=[embed,logembed], view=self)
        except Exception as e:
          self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 20 | ' + str(e))
        self.stop()
        self.checker.stop()
        return await extra_functions.reloadMessageDrop(bot=self.bot, guild=self.response.guild)
      self.countToObsticle += 1
      
      
  async def on_timeout(self):
    self.finished = True
    self.checker.stop()
    if len(self.peopleDamage) != 0:
      end_string = '```css\n[Rank] | {.Dmg / Miss.} | Treater\n==========================================\n'
      sorted_damage = dict(sorted(self.peopleDamage.items(), key=lambda item: item[1], reverse=True))
      i = 0
      for person in sorted_damage:

        try:
          sorted_damage[person]
        except (IndexError, KeyError, TypeError):
          break
        
        name = self.guild.get_member(person).display_name
        if i == 10:
          break
        end_string += " " + "[" + str(i+1).zfill(2) + "]" + "  |   " + str(math.floor(sorted_damage[person])).zfill(3) + " / " + str(self.peopleMissCount[person]).zfill(2) + "     | " + name[:13] + "\n"
        i += 1

      end_string += '```'

      embed = discord.Embed(title='The Battle has been Lost!',description='⠀\n' + self.descriptions['loss'][0] + '\n⠀', color=discord.Color.blurple())
      embed.set_image(url=self.images[5])
      self.clear_items()
      try:
        await self.response.edit(embed=embed, view=self)
      except Exception as e:
        self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 21 | ' + str(e))
      await asyncio.sleep(5)
      embed = discord.Embed(title='The Battle has been Lost!',description='⠀\n' + self.descriptions['loss'][1] + '\n⠀', color=discord.Color.blurple())
      embed.set_image(url=self.images[5])
      embed.set_footer(text='Try again next time!')

      logembed = discord.Embed(title='Battle Results',description='⠀\n' + end_string +'\n⠀', color=discord.Color.greyple())
      try:
        await self.response.edit(embeds=[embed,logembed], view=self)
      except Exception as e:
        self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 22 | ' + str(e))
      self.stop()
      return await extra_functions.reloadMessageDrop(bot=self.bot, guild=self.response.guild)
    else:
      embed = discord.Embed(title='The Headless Horseman has left',description='⠀\n' + self.descriptions['idle'] + '\n⠀', color=discord.Color.purple())
      embed.set_image(url=self.images[5])
      self.clear_items()
      self.stop()
      try:
        await self.response.edit(embed=embed, view=self)
      except Exception as e:
        self.bot.logger.error(extra_functions.printGuildDetails(self.guild) + ' - Boss Edit Fail 23 | ' + str(e))
      return await extra_functions.reloadMessageDrop(bot=self.bot, guild=self.response.guild)


  def aftermath(self, message):
    self.message = message

class SpawnBoss: #Do intro with Links View then create actual view when battle starts
  async def spawnBoss(self, message):
    try:
      self.bot.messages[str(message.guild.id)]['activeMessage'] = True
      settings = await extra_functions.getGuildSettings(self.bot, message.guild)

      images = ['https://cdn.discordapp.com/attachments/782835367085998080/1028735160008572968/Prephase_1.png','https://cdn.discordapp.com/attachments/782835367085998080/1028735159320719441/Phase_1.png','']
      descriptions = json.load(open('./JSON/boss.json'))
      try:
        view = message_spawn(bot=self.bot, settings=settings, descriptions=descriptions, guild=message.guild)
        embed = discord.Embed(title='Something is happening',description='⠀\n' + descriptions['intro'][0] + '\n⠀', color=discord.Color.purple())
        embed.set_image(url=images[0])
        channel = message.guild.get_channel(random.choice(settings['channel_id']))
        m = await channel.send(embeds= [embed], view=view)
        view.response = m
        self.bot.logger.info(extra_functions.printGuildDetails(message.guild) + ' - Boss Message Sent')

        await asyncio.sleep(8)
        embed = discord.Embed(title='The Headless Horseman',description='', color=discord.Color.red())
        embed.set_author(name='Face Of Death')
        embed.set_image(url=images[1])
        await m.edit(embed=embed)

        await asyncio.sleep(5)
        view.phase = 1
        self.bot.logger.info(extra_functions.printGuildDetails(message.guild) + ' - Boss Message Started')
      except:
        self.bot.logger.error(extra_functions.printGuildDetails(message.guild) + ' - Boss Message Failed')
        return await extra_functions.reloadMessageDrop(bot=self.bot, guild=message.guild)
    except:
      return await extra_functions.reloadMessageDrop(bot=self.bot, guild=message.guild)

  async def spawnBossVC(bot, guild):
    try:
      bot.messages[str(guild.id)]['activeMessage'] = True
      settings = await extra_functions.getGuildSettings(bot, guild)

      images = ['https://cdn.discordapp.com/attachments/782835367085998080/1028735160008572968/Prephase_1.png','https://cdn.discordapp.com/attachments/782835367085998080/1028735159320719441/Phase_1.png','']
      descriptions = json.load(open('./JSON/boss.json'))
      try:
        view = message_spawn(bot=bot, settings=settings, descriptions=descriptions, guild=guild)
        embed = discord.Embed(title='Something is happening',description='⠀\n' + descriptions['intro'][0] + '\n⠀', color=discord.Color.purple())
        embed.set_image(url=images[0])
        channel = guild.get_channel(random.choice(settings['channel_id']))
        m = await channel.send(embeds= [embed], view=view)
        view.response = m
        bot.logger.info(extra_functions.printGuildDetails(guild) + ' - Boss Message Sent')

        await asyncio.sleep(8)
        embed = discord.Embed(title='The Headless Horseman',description='', color=discord.Color.red())
        embed.set_author(name='Face Of Death')
        embed.set_image(url=images[1])
        await m.edit(embed=embed)

        await asyncio.sleep(5)
        view.phase = 1
        bot.logger.info(extra_functions.printGuildDetails(guild) + ' - Boss Message Started')
      except:
        bot.logger.error(extra_functions.printGuildDetails(guild) + ' - Boss Message Failed')
        return await extra_functions.reloadMessageDrop(bot=bot, guild=guild)
    except:
      return await extra_functions.reloadMessageDrop(bot=bot, guild=guild)

  async def spawnBossInteraction(self, interaction):
    try:
      self.bot.messages[str(interaction.guild.id)]['activeMessage'] = True
      settings = await extra_functions.getGuildSettings(self.bot, interaction.guild)

      images = ['https://cdn.discordapp.com/attachments/782835367085998080/1028735160008572968/Prephase_1.png','https://cdn.discordapp.com/attachments/782835367085998080/1028735159320719441/Phase_1.png','']
      descriptions = json.load(open('./JSON/boss.json'))
      try:
        view = message_spawn(bot=self.bot, settings=settings, descriptions=descriptions, guild=interaction.guild)
        embed = discord.Embed(title='Something is happening',description='⠀\n' + descriptions['intro'][0] + '\n⠀', color=discord.Color.purple())
        embed.set_image(url=images[0])
        channel = interaction.guild.get_channel(random.choice(settings['channel_id']))
        m = await channel.send(embeds= [embed], view=view)
        view.response = m
        self.bot.logger.info(extra_functions.printGuildDetails(interaction.guild) + ' - Boss Message Sent')

        await asyncio.sleep(8)
        embed = discord.Embed(title='The Headless Horseman',description='', color=discord.Color.red())
        embed.set_author(name='Face Of Death')
        embed.set_image(url=images[1])
        await m.edit(embed=embed)

        await asyncio.sleep(5)
        view.phase = 1
        self.bot.logger.info(extra_functions.printGuildDetails(interaction.guild) + ' - Boss Message Started')
      except:
        self.bot.logger.error(extra_functions.printGuildDetails(interaction.guild) + ' - Boss Message Failed')
        return await extra_functions.reloadMessageDrop(bot=self.bot, guild=interaction.guild)
    except:
      return await extra_functions.reloadMessageDrop(bot=self.bot, guild=interaction.guild)
