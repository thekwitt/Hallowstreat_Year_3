import time, collections
import discord, random, asyncio
from discord.ext.tasks import loop
from discord import app_commands
from discord.ext import commands
from typing import List, Optional
from extra.discord_functions import extra_functions

class messageButton(discord.ui.Button['page_viewer']):
    def __init__(self, type: int, emoji, target):

      super().__init__(style=discord.ButtonStyle.primary, emoji=emoji, row=0)
      self._type = type
      self.target = target

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: page_viewer = self.view

        if interaction.user.id != view.user_id:
            return await interaction.response.send_message("You can\'t control this candy bag message! Try it yourself with **/candybag**.", ephemeral=True)

        if self._type == 0:
            if view.page == 0:
                try:
                    return await interaction.response.defer()
                except:
                    pass
            else:
                view.page -= 1
        elif self._type == 1:
            if view.page == view.max_page - 1:
                try:
                    return await interaction.response.defer()
                except:
                    pass
            else:
                view.page += 1

        candy_bag = view.candy_bag
        candy_string = ''
        i = 0
        j = 0
        k = 0
        for candy in candy_bag:

            if k < view.page * 25:
                k += 1
            else:
                try:
                    candy_bag[candy]
                except (IndexError, KeyError):
                    break 

                if i <= 4:
                    candy_string += candy + ' x ' + str(candy_bag[candy]).zfill(3) + '⠀⠀⠀'
                else:
                    i = 0
                    candy_string += '\n\n' + candy + ' x ' + str(candy_bag[candy]).zfill(3) + '⠀⠀⠀'

                j += 1
                i += 1

                if j >= 25:
                    break
            
        embed = discord.Embed(title= self.target.name + '\'s Candy Bag', description='⠀\n' + candy_string + '\n⠀', color=discord.Color.orange())
        embed.set_footer(text='Controlled by ' + interaction.user.name + ' | Page ' + str(view.page + 1) + '/' + str(view.max_page) + ' | Use Arrows to switch pages')

        await interaction.response.edit_message(embed=embed, view=view)



class page_viewer(discord.ui.View):
  children: List[messageButton]

  def __init__(self, interaction, candy_bag, user_id, target):
    super().__init__(timeout=120)

    self.page = 0
    self.user_id = user_id
    self.max_page = int((len(candy_bag) - 1) / 25) + 1
    self.candy_bag = candy_bag
    self.interaction = interaction
    self.target = target

    for x in range(2):
        self.add_item(messageButton(x, ['⬅️', '➡️'][x], self.target))

  async def on_timeout(self):
    for child in self.children:
        child.disabled = True
    await self.response.edit(view=self)


class candy_viewer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="candy_bag",description='Display a user\'s candy bag')
    @app_commands.describe(user='Another user\'s candy bag')
    async def candy_bag(self, interaction: discord.Interaction, user: Optional[discord.User]) -> None:
        if(await extra_functions.readyCheck(self.bot, interaction) == True):
            # REQUIRED
            extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Candy Bag Command Execute')
            if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
                return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
            await extra_functions.beforeCommand(self.bot, interaction)
            # DO CODE BELOW

            u_obj = interaction.user
            if user != None:
                u_obj = user

            if await self.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", u_obj.id, interaction.guild_id) == None:
                await extra_functions.Insert_User(self.bot,interaction.guild.id,u_obj.id)   

            user_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", u_obj.id, interaction.guild_id)
            if len(user_data["candy_bag"]) == 0:
                embed = extra_functions.embedBuilder("🧺  " + u_obj.name + "'s Empty Candy Bag  🧺","Get some candy first.","Collect Candy by interacting to candy messages",0xE56A6A)
                return await interaction.response.send_message(embed=embed)

            user_bag = [c for c in self.bot.candy if int(c['id']) in user_data['candy_bag']]

            candy_bag = {}

            for candy in user_bag:
                if not candy['emoji'] in candy_bag.keys():
                    candy_bag[str(candy['emoji'])] = user_data['candy_bag'].count(int(candy['id']))

            candy_string = ''

            i = 0
            j = 0
            for candy in candy_bag:

                try:
                    candy_bag[candy]
                except (IndexError, KeyError):
                    break 

                if i <= 4:
                    candy_string += candy + ' x ' + str(candy_bag[candy]).zfill(3) + '⠀⠀⠀'
                else:
                    i = 0
                    candy_string += '\n\n' + candy + ' x ' + str(candy_bag[candy]).zfill(3) + '⠀⠀⠀'

                j += 1
                i += 1

                if j >= 25:
                    break
                
            embed = discord.Embed(title= u_obj.name + '\'s Candy Bag', description='⠀\n' + candy_string + '\n⠀', color=discord.Color.orange())
            embed.set_footer(text='Controlled by ' + interaction.user.name + ' | Page 1/' + str(int((len(candy_bag) - 1) / 25) + 1) + ' | Use Arrows to switch pages')

            view = page_viewer(interaction, candy_bag, interaction.user.id, u_obj)

            await interaction.response.send_message(embed=embed, view=view)

            view.response = await interaction.original_response()
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(candy_viewer(bot))