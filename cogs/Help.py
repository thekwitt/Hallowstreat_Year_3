import discord
from discord import app_commands, Interaction
from discord.ext import commands
from discord.ext.commands import GroupCog
from discord.app_commands import Choice
from extra.discord_functions import extra_functions
from typing import Literal

class Help(GroupCog, group_name='help', group_description='Get or Set Settings for the bot on your server!'):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name="manual",description='All overviews of the bot.')
  @app_commands.describe(manual='What kind of overview.')
  @app_commands.choices(manual = [Choice(name="Overview of Bot", value="overview"), Choice(name="Overview of Candy", value="candy"), Choice(name="Overview of Events", value="events"), Choice(name="Overview of Giving and Scaring", value="giving")])
  async def manual(self, interaction: discord.Interaction, manual: Choice[str]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      manual = manual.value
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='manual Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW
      if manual == 'overview':
        embed = discord.Embed(title='Overview of Bot', description='HallowsTreat is a fun month-long Candy collecting bot designed to give Halloween a new spin and twist. This bot features interactive events, player to player commands, and customizable options that allow the bot to scale to any server of any size.\n\nInteractive events such as candy drops and boss battles (Available October 7th) will spawn on the server based on how active it is. You can collect candy with these events and use commands to either treat your friends or trick your enemies.')
        embed.set_footer(text='See other overviews with /help')
        await interaction.response.send_message(embed=embed)
      elif manual == 'events':
        embed = discord.Embed(title='Overview of Interactive Events', description='There are two different kinds of events that can occur. One of them is candy drops. Candy drops allow users to collect candy in more than 10 different varieties. All you need to do is select the correct prompt that the message gives and you get a piece of candy.\n\nThe second event is called a boss battle. In this event, players of the community join forces to defeat a powerful foe called the headless horseman in two minutes. Throughout the battle, you will need to read the second box prompt that tells you what to do whether it is to hit the enemy or avoid attacks or counter-powerful strikes. When defeated, The rewards that players get will be golden candy which is legendary candy that you can add to your collection. These pieces of candy cannot be eaten. (Releases October 7th)')
        embed.set_footer(text='See other overviews with /help')
        await interaction.response.send_message(embed=embed)
      elif manual == 'giving':
        embed = discord.Embed(title='Overview of Giving and Scaring', description='You can treat your friends by giving away your candy. With the giving command, you can select any piece of candy that is in your bag and give it to another player.\n\nYou can trick your enemies with the scare command. When you scare someone you have a 50"%" chance for it to either fail or succeed. When a player is scared, they lose a percentage of their entire candy bag but only a small percentage.')
        embed.set_footer(text='See other overviews with /help')
        await interaction.response.send_message(embed=embed)
      elif manual == 'candy':
        embed = discord.Embed(title='Overview of Candy', description='Candy is a fun interactable item that you can collect throughout the bot. There is over 150 different varieties of candy that you can collect and eat.\n\nYou can gain several bonuses for eating different types of candy. These bonuses can help you gather more candy sabotage your friends, or deal more damage against the dreaded headless horseman.\n\n**These bonuses cannot stack and only last one hour**')
        embed.set_footer(text='See other overviews with /help')
        await interaction.response.send_message(embed=embed)

  @app_commands.command(name="faq",description='Common questions you may have')
  @app_commands.describe(manual='What kind of overview.')
  @app_commands.choices(manual = [Choice(name="How do I start the bot?", value="start"), Choice(name="Why aren\'t drops spawning?", value="drop"), Choice(name="Where are the slash commands?", value="slash"), Choice(name="I got \"Interaction Failed\". What does that mean?", value="interaction")])
  async def faq(self, interaction: discord.Interaction, manual: Choice[str]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      manual = manual.value
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='faq Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW
      if manual == 'start':
        embed = discord.Embed(title='❓   How do I start the bot?   ❓', description='⠀\nWhen you invite the bot, you will need to initialize the bot by using the **/setchannel** command! If the command throws out an error, make sure the bot has two key factors. \n\nServer and Channel permission to send embedded messages outside of slash commands and use external emojis.\n\n⠀')
        embed.set_footer(text='See other faqs with /help')
        await interaction.response.send_message(embed=embed)
      elif manual == 'interaction':
        embed = discord.Embed(title='❓   I got "Interaction Failed". What does that mean?   ❓', description='⠀\nOn rare occasions, discord doesn\'t send all the info the bot needs to get the job done or doesn\'t accept the bot send them info.\n\nOn collecting drops, if you get this message, you got the drop but it just didn\'t allow the bot to send the message through.\n\nOn commands, the bot will detect if this happens and restart any cooldowns you may have from using the command but nothing will be erased from your inventory.\n⠀')
        embed.set_footer(text='See other faqs with /help')
        await interaction.response.send_message(embed=embed)
      elif manual == 'drop':
        embed = discord.Embed(title='❓   Why aren\'t drops spawning?   ❓', description='⠀\nThere are a few reasons why the bot does not spawn drops. The first reason could be denied access to send embedded messages and use external emojis.\
					\n\nPlease make sure that **View Channel, Send Messages, Embed Links, and Use External Emoji** Permissions are ticked in the role and/or channel (only if you edit the channel to only have certain roles have sending perms).\
					\n\nAnother reason could be that the timer has not gone off yet. Please use the **/checkdrop** command to verify that it has not triggered.\
          \n\nPlease keep in mind that slash commands can bypass these permissions because Discord requires a direct response from them. Drops send messages without discord\'s bypass.\
					\n\nIf any of these did not work, please head over to the support server with **/help support**.\n⠀')
        embed.set_footer(text='See other faqs with /help')
        await interaction.response.send_message(embed=embed)
      elif manual == 'slash':
        embed = discord.Embed(title='❓   Where are the slash commands?   ❓', description='⠀\nSometimes discord may need time to have slash commands show up. It takes up to an hour for current and new commands to show up in servers if they do not appear.\
					\n\nOtherwise if you have more than 25 bots, it is possible that slash commands are prioritized to those first 25 bots. How it works is that only the first 25 invited bots can have their commands prioritized for your server.\
					\n\nYou will need to remove those bots in order to use this bot\'s functionality.\n⠀')
        embed.set_footer(text='See other faqs with /help')
        await interaction.response.send_message(embed=embed)

  @app_commands.command(name="commands",description='Everything and anything about the commands!')
  @app_commands.describe(manual='What commands do you need explained?')
  @app_commands.choices(manual = [Choice(name="Candy Commands", value="candy"), Choice(name="Info Commands", value="info"), Choice(name="Mod Tools", value="mod"), Choice(name="Settings Commands", value="settings")])
  async def commands(self, interaction: discord.Interaction, manual: Choice[str]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      manual = manual.value
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='commands Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW
      if manual == 'candy':
        embed = discord.Embed(title='📙   Candy Commands   📙')
        embed.add_field(name = '/candy_collection', value = 'See every type of candy a user has collected.',inline=False)
        embed.add_field(name = '/candy_bag', value = 'View a user\'s candy bag.',inline=False)
        embed.add_field(name = '/candylookup', value = 'Look up a piece of candy and its bonus!',inline=False)
        embed.add_field(name = '/bonuscandylookup', value = 'Look up a golden piece of candy and its bonus!',inline=False)
        embed.add_field(name = '/collect_vote_bonus', value = 'Get more candy just by voting!',inline=False)
        embed.add_field(name = '/eatcandy', value = 'Eat a piece of candy and gain a bonus!',inline=False)
        embed.add_field(name = '/scare', value = 'Scare someone to get their candy!',inline=False)
        embed.add_field(name = '/givecandy', value = 'Give a user a piece of candy!',inline=False)
        embed.add_field(name = '/bulkgivecandy', value = 'Give a user a piece of candy in random bulk form!',inline=False)
        embed.set_footer(text='See other commands with /help')
        await interaction.response.send_message(embed=embed)
      elif manual == 'info':
        embed = discord.Embed(title='📙   Info Commands   📙')
        embed.add_field(name = '/help', value = 'See everything about the bot.',inline=False)
        embed.add_field(name = '/quick_guide', value = 'Overall walkthrough for users and staff!',inline=False)
        embed.add_field(name = '/leaderboard', value = 'Top 100 players of the bot',inline=False)
        embed.add_field(name = '/card', value = 'Profile card with basic stats',inline=False)
        embed.add_field(name = '/support', value = 'A direct link to the support server!',inline=False)
        embed.add_field(name = '/patreon_link', value = 'The direct link to patreon and what you get for supporting!',inline=False)
        embed.add_field(name = '/roadmap', value = 'See the progress of all the updates for this bot!',inline=False)
        embed.set_footer(text='See other commands with /help')
        await interaction.response.send_message(embed=embed)
      elif manual == 'mod':
        embed = discord.Embed(title='📙   Mod Commands   📙')
        embed.add_field(name = '/setup', value = 'Setup the server for your bot!',inline=False)
        embed.add_field(name = '/setup_patreon', value = 'Set up your patreon subscription with the bot using your email!',inline=False)
        embed.add_field(name = '/status_patreon', value = 'See if your server has premium activated.',inline=False)
        embed.add_field(name = '/erase_member', value = 'Erase a member from your server\'s database. (CANNOT UNDO)',inline=False)
        embed.add_field(name = '/erase_members', value = 'Erase members with a certain role from your server\'s database. (CANNOT UNDO)',inline=False)
        embed.add_field(name = '/erase_guild', value = 'Erase a server\'s database. (CANNOT UNDO)',inline=False)
        embed.add_field(name = '/spawn_candy_drop', value = '**(Premium Only)** Spawns a candy message at will!',inline=False)
        embed.add_field(name = '/spawn_headless_horseman', value = '**(Premium Only)** Spawns a boss message at will!',inline=False)
        embed.add_field(name = '/drop_clock', value = 'See when the next drop will spawn.',inline=False)
        embed.add_field(name = '/reload_drop', value = 'Is the drop stuck? Reload with this command.',inline=False)        
        embed.add_field(name = '/add_candy_role', value = '**(Premium Only)** Add candy to all users of a role.',inline=False)        
        embed.add_field(name = '/add_channel_spawn', value = 'Add a channel to the event spawner.',inline=False)        
        embed.add_field(name = '/remove_channel_spawn', value = 'Remove a channel to the event spawner.',inline=False)        
        embed.add_field(name = '/add_candy_user', value = 'Add candy to a single user.',inline=False)
        embed.add_field(name = '/remove_candy_user', value = 'Remove candy from a single user.',inline=False)        
        embed.set_footer(text='See other commands with /help. Setting Commands are under /help commands settings')
        await interaction.response.send_message(embed=embed)
      elif manual == 'settings':
        embed = discord.Embed(title='📙   Settings Commands   📙')
        embed.add_field(name = 'change_message_count_for_drop', value = 'Change the amount of messages it takes for a drop to spawn.',inline=False)
        embed.add_field(name = 'change_time_interval_for_drop', value = 'Change the time it takes for drops to spawn.',inline=False)
        embed.add_field(name = 'change_drop_duration', value = '**(Premium Only)** Change how long a drop lasts.',inline=False)
        embed.add_field(name = 'enable_giving', value = 'Enable the /givecandy command on the server.',inline=False)
        embed.add_field(name = 'enable_scare', value = 'Enable the /scare command on the server.',inline=False)
        embed.add_field(name = 'change_candy_per_drop', value = '**(Premium Only)** Change how many pieces of candy users get per drop.',inline=False)     
        embed.add_field(name = 'change_users_per_drop', value = '**(Premium Only)** Change how many users can access a drop.',inline=False)        
        embed.add_field(name = 'change_percent_lost_scare', value = '**(Premium Only)** Change the percentage of candy lost when using /scare',inline=False)           
        embed.add_field(name = 'change_bulk_give_limit', value = 'Change the limit of how much a bulk give can do at a time.',inline=False)     
        embed.add_field(name = 'view_settings', value = 'Displays every setting you have access to!',inline=False)        
        embed.add_field(name = 'change_boss_difficulty', value = 'Change the difficulty of the Headless Horseman from Easy to Headless (Extreme)',inline=False)           
        embed.add_field(name = 'change_boss_spawn_chance', value = 'Change the percentage chance of a boss spawning compared to candy.',inline=False)           
        embed.set_footer(text='See other commands with /help. Mod commands are under /help commands mod')
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Help(bot))