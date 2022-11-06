from argparse import RawDescriptionHelpFormatter
import discord, math, time, random
from discord import app_commands, Interaction
from discord.ext import commands
from discord.app_commands import AppCommandError
from extra.discord_functions import extra_functions

class Links(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Patreon Link', url='https://www.patreon.com/thekwitt'))
        self.add_item(discord.ui.Button(label='Support Link', url='https://discord.com/invite/ZNpCNyNubU'))

class RoadmapLinks(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Roadmap Link', url='https://trello.com/b/aMJArKyM/hallowstreat'))
        self.add_item(discord.ui.Button(label='Support Link', url='https://discord.com/invite/ZNpCNyNubU'))

class Links2(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Topgg Review Link', url='https://top.gg/bot/886391809939484722'))
        self.add_item(discord.ui.Button(label='Topgg Vote Link', url='https://top.gg/bot/886391809939484722/vote'))

class PatreonLink(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Patreon Link', url='https://www.patreon.com/thekwitt'))

class SupportLink(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Support Link', url='https://discord.com/invite/ZNpCNyNubU'))

class Patreon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="road_map",description='Keep track of what the dev is cooking!')
    async def roadmap(self, interaction: discord.Interaction):
        if(await extra_functions.readyCheck(self.bot, interaction) == True):
            # REQUIRED
            extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='patreon_setup Command Execute')
            await extra_functions.beforeCommand(self.bot, interaction)
            # DO CODE BELOW

            embed = discord.Embed(title='🚧   Roadmap   🚧', description= '⠀\nAs a lot of people know. I am very transparent with my work and I want everyone to be the same page as I am!\n\nThe link below is what I am currently working on! Check it out!\n⠀')
            embed.set_footer(text = 'If you wanna suggest something, create a post in the support server!')

            return await interaction.response.send_message(embed=embed, view=RoadmapLinks())

    @app_commands.command(name="vote_and_review",description='Get a direct link to voting and reviewing!')
    async def vote_and_review(self, interaction: discord.Interaction):
        if(await extra_functions.readyCheck(self.bot, interaction) == True):
            # REQUIRED
            extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='patreon_setup Command Execute')
            await extra_functions.beforeCommand(self.bot, interaction)
            # DO CODE BELOW

            embed = discord.Embed(title='🔗   Top.gg Links   🔗', description= '⠀\nMaking the bot known to everyone helps spread the fun twist to Halloween for everyone on Discord. With your votes and reviews, you can not only show the love and opinions you have for this bot but also show me, the creator, what you think as well!\n\nIf you have just a small amount of time, please consider a vote or review on what you think of the bot so far! Every vote and review sounds as a big thank you from me! :D\n⠀')

            return await interaction.response.send_message(embed=embed, view=Links2())

    @app_commands.command(name="patreon_link",description='Get the link for patreon and see what it comes with!')
    async def premium(self, interaction: discord.Interaction):
        if(await extra_functions.readyCheck(self.bot, interaction) == True):
            # REQUIRED
            extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='patreon_setup Command Execute')
            await extra_functions.beforeCommand(self.bot, interaction)
            # DO CODE BELOW

            embed = discord.Embed(title='💵   Patreon Premium Page   💵', description= '⠀\nAs you may have guessed, running and maintaining bots everyone to enjoy is not cheap. With your help, it is possibly to keep this train rolling and make greater things along the way!\n\n**DISCLAIMER: I WILL NEVER CHARGE ANYONE TO USE THE BOT\'S FULL FUNCTIONALITY! ALL OF MY PRODUCTS WILL *ALWAYS* BE FREE. THIS IS JUST AN EXTRA BONUS OF FEATURES THAT CAN BENEFIT SOME SERVERS AND COMMUNITIES.**\n\nUse the button below to visit the patreon so not only you can help support the project but also get some sweet perks to maximize the usage of this bot and future ones as well! You can also support me for free by leaving a review and/or giving a vote! Every vote and review helps a lot!\n⠀')
            embed.add_field(name='Current Features',value='Spawning Drops at will.\nAdd up to 15 channel spawns instead of 3!\nChange specific amounts of food for farmer\'s markets and sacks of food.\nSkip voting and collect bonuses for free!\nAdd food to users via role for easy transfering!')
            embed.set_footer(text = 'For any questions/concerns please visit the official TheKWitt server!')

            return await interaction.response.send_message(embed=embed, view=Links())

    @app_commands.command(name="support",description='Get the link to the support server.')
    async def support(self, interaction: discord.Interaction):
        if(await extra_functions.readyCheck(self.bot, interaction) == True):
            # REQUIRED
            extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='patreon_setup Command Execute')
            await extra_functions.beforeCommand(self.bot, interaction)
            # DO CODE BELOW

            embed = discord.Embed(title='🔗   Support Server!   🔗', description= '⠀\nClick the button below to visit the support server!\n⠀')

            return await interaction.response.send_message(embed=embed, view=SupportLink())

    @app_commands.command(name="setup_patreon",description='Setup your email and activate the bot! (Your email will not be displayed)')
    @app_commands.describe(email='The email your patreon subscription is setup with.')
    async def patreon_setup(self, interaction: discord.Interaction, email: str):
        if(await extra_functions.readyCheck(self.bot, interaction) == True):
            # REQUIRED
            extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='patreon_setup Command Execute')
            await extra_functions.beforeCommand(self.bot, interaction)

            #if interaction.user.guild_permissions.manage_channels == False:
            #    return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

            # DO CODE BELOW
        
            if await extra_functions.checkEmail(self.bot, email) == False:
                embed = discord.Embed(title='Looks like your email is not registed', description= '⠀\nSometimes it takes an hour for your email to register. If you already waited that long and your email is still not registered, check out the support server below and DM TheKWitt! Otherwise, consider getting the premium version for only **two dollars**!\n⠀')

                return await interaction.response.send_message(embed=embed, view=Links(), ephemeral=True)

            raw_data = await self.bot.patreon.fetch('SELECT * FROM existing;')
            bought_existing = [exist for exist in raw_data if exist['guild_id'] == interaction.guild_id]

            dedicated_json = self.bot.dedicated_patreon
            dedicated = dedicated_json['premium']
            dedicated_existing = [exist for exist in dedicated if exist['guild_id']  == interaction.guild_id]


            if len(bought_existing) != 0 or len(dedicated_existing) != 0:
                return await interaction.response.send_message(content='Good news! This server is already registered for premium!', ephemeral=True)

            await self.bot.patreon.execute('UPDATE existing SET guild_id = $1 WHERE email = $2', interaction.guild_id, email)
            await interaction.response.send_message(content='This email is now enabled and your server is configured for bot use! Congrats!', ephemeral=True)

    @app_commands.command(name="status_patreon",description='Check if your server has been setup with premium')
    async def patreon_status(self, interaction: discord.Interaction):
        if(await extra_functions.readyCheck(self.bot, interaction) == True):
            # REQUIRED
            extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='status_patreon Command Execute')
            await extra_functions.beforeCommand(self.bot, interaction)

            #if interaction.user.guild_permissions.manage_channels == False:
            #    return await interaction.response.send_message("You don't have permission to use this command. You need **manage channel** perms to use this command.", ephemeral=True)

            # DO CODE BELOW
        
            raw_data = await self.bot.patreon.fetch('SELECT * FROM existing;')
            existing = [data for data in raw_data if data['guild_id'] == interaction.guild_id]

            dedicated_json = self.bot.dedicated_patreon
            dedicated = dedicated_json['premium']
            dedicated_existing = [exist for exist in dedicated if exist['guild_id']  == interaction.guild_id]

            if len(existing) != 0 or len(dedicated_existing) != 0:
                return await interaction.response.send_message(content='Good news! This server is already registered for premium!', ephemeral=True)

            await interaction.response.send_message(content='Looks like this server has not been setup yet. Consider using **/setup_patreon**. If this server has not been setup yet, please consider using the support server link below or if you haven\'t already purchased yet, check out the patreon link below.', ephemeral=True, view=Links())
       

    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Patreon(bot))