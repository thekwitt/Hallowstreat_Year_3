import time, collections
import discord, random, asyncio
from discord.ext.tasks import loop
from discord import app_commands
from discord.ext import commands
from typing import List, Optional
from extra.discord_functions import extra_functions

class messageButton(discord.ui.Button['page_viewer']):
    def __init__(self, type: int, emoji):

      super().__init__(style=discord.ButtonStyle.primary, emoji=emoji, row=0)
      self._type = type

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: page_viewer = self.view

        if interaction.user.id != view.changer.id:
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

        missing = '<:missing:1023357161906114680>'

        embed = discord.Embed(title= view.user_id.name + '\'s Candy Collection', color=discord.Color.orange())
        embed.set_footer(text='Controlled by ' + interaction.user.name + ' | Page ' + str(view.page + 1) + '/' + str(view.max_page) + ' | Use Arrows to switch pages')

        for t in view.types[view.page]:
            temp_array = [c for c in view.bot.candy if c['type'] == t]
            temp_collect = []
            temp_int = 0
            for temp in temp_array:
                if temp['has'] == True:
                    temp_collect.append(temp['emoji'])
                else:
                    temp_collect.append(missing)

                temp_int += 1
                if temp_int >= 15:
                    embed.add_field(name=t, value=' '.join(temp_collect), inline=False)
                    temp_collect = []
                    temp_int = 0
            embed.add_field(name=t, value=' '.join(temp_collect), inline=False)            

        await interaction.response.edit_message(embed=embed, view=view)



class page_viewer(discord.ui.View):
  children: List[messageButton]

  def __init__(self, interaction, candy_bag, user_id, types, bot, changer):
    super().__init__(timeout=120)

    self.changer = changer
    self.bot = bot
    self.types = types
    self.page = 0
    self.user_id = user_id
    self.max_page = len(types)
    self.candy_bag = candy_bag
    self.interaction = interaction

    for x in range(2):
        self.add_item(messageButton(x, ['⬅️', '➡️'][x]))

  async def on_timeout(self):
    for child in self.children:
        child.disabled = True
    await self.response.edit(view=self)


class candy_collection(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="candy_collection",description='Display a user\'s candy collection')
    @app_commands.describe(user='Another user\'s candy collection')
    async def candy_collection(self, interaction: discord.Interaction, user: Optional[discord.User]) -> None:
        if(await extra_functions.readyCheck(self.bot, interaction) == True):
            # REQUIRED
            extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Candy Collection Command Execute')
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
            if len(user_data["candy_completion"]) == 0:
                embed = extra_functions.embedBuilder("🧺  " + u_obj.name + "'s Empty Candy Bag  🧺","Get some candy first.","Collect Candy by interacting to candy messages",0xE56A6A)
                return await interaction.response.send_message(embed=embed)

            candy_bag = [c for c in self.bot.candy if c['type'] != '']
            types = [['Corn', 'Banana', 'Chewy', 'Gums'], ['Soda', 'Cane', 'Swirls', 'Swag'], ['Wraps', 'Suckers', 'Jawbreakers'], ['Gummy', 'Golden']]

            for candy in candy_bag:
                candy['has'] = int(candy['id']) in user_data['candy_completion']

            missing = '<:missing:1023357161906114680>'
 
            embed = discord.Embed(title= u_obj.name + '\'s Candy Collection', color=discord.Color.orange())
            embed.set_footer(text='Controlled by ' + interaction.user.name + ' | Page 1/' + str(len(types)) + ' | Use Arrows to switch pages')

            for t in types[0]:
                temp_array = [c for c in self.bot.candy if c['type'] == t]
                temp_collect = []
                temp_int = 0
                for temp in temp_array:
                    if temp['has'] == True:
                        temp_collect.append(temp['emoji'])
                    else:
                        temp_collect.append(missing)

                    temp_int += 1
                    if temp_int >= 15:
                        embed.add_field(name=t, value=' '.join(temp_collect), inline=False)
                        temp_collect = []
                        temp_int = 0
                embed.add_field(name=t, value=' '.join(temp_collect), inline=False) 

            view = page_viewer(interaction, candy_bag, u_obj, types, self.bot, interaction.user)

            await interaction.response.send_message(embed=embed, view=view)

            view.response = await interaction.original_response()
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(candy_collection(bot))