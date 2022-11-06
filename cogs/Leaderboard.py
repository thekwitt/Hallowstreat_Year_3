import discord
from discord import app_commands, Interaction
from discord.ext import commands
from discord.app_commands import AppCommandError
from extra.discord_functions import extra_functions
from typing import List, Optional

class messageButton(discord.ui.Button['page_viewer']):
    def __init__(self, type: int, emoji):

      super().__init__(style=discord.ButtonStyle.primary, emoji=emoji, row=0)
      self._type = type

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: page_viewer = self.view

        if interaction.user.id != view.user_id:
            return await interaction.response.send_message("You can\'t control this leaderboard! Try it yourself with **/leaderboard**.", ephemeral=True)

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

        string = "```css\n[Rank] | {.Candy.} | Treater\n==========================================\n"
        i = 0
        fucking_eat_my_ass = False
        for user in view.users:
          if i >= view.page * 10:
            try:
              user[0]
            except (IndexError, KeyError, TypeError):
              break

            if(user[0] == interaction.user.id):
                fucking_eat_my_ass = True

            try:
              u = interaction.guild.get_member(user[0])
              if u != None:
                string += " " + "[" + str(i+1).zfill(2) + "]" + "  |   " + str(user[1]).zfill(5) + "   | " + u.display_name[:18] + "\n"
            except Exception as e:
              try:
                u = await interaction.guild.fetch_member(user[0])
                if u != None:
                  string += " " + "[" + str(i+1).zfill(2) + "]" + "  |   " + str(user[1]).zfill(5) + "   | " + u.display_name[:18] + "\n"
              except Exception as e:
                self.bot.logger.error(user + ' | Leaderboard Member Get Failed')
          
          i += 1
          
          if i >= view.page * 10 + 10:
            break

        if not fucking_eat_my_ass:
          if view.index != -1:
            string += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n " + "[" + str(view.index+1).zfill(2) + "]" + "  |   " + str(view.users[view.index][1]).zfill(5) + "   | " + interaction.user.display_name[:18] + "\n"
          else:
            string += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n " + "[" + str(interaction.guild.member_count) + "]  |   00000   | " + interaction.user.display_name[:18] + "\n"

        string += '```'
        embed = extra_functions.embedBuilder(interaction.guild.name + "'s Leaderboard",string,"Page 1/" + str(view.max_page)  + " | Use the button to swap pages",0xFF42AE)
        embed.set_footer(text='Controlled by ' + interaction.user.name + ' | Page ' + str(view.page + 1) + '/' + str(view.max_page) + ' | Use Arrows to switch pages')

        await interaction.response.edit_message(embed=embed, view=view)



class page_viewer(discord.ui.View):
  children: List[messageButton]

  def __init__(self, interaction, users, index, max_page, user_id):
    super().__init__(timeout=120)

    self.page = 0
    self.users = users
    self.max_page = max_page
    self.interaction = interaction
    self.index = index
    self.user_id = user_id

    for x in range(2):
        self.add_item(messageButton(x, ['⬅️', '➡️'][x]))

  async def on_timeout(self):
    for child in self.children:
        child.disabled = True
    await self.response.edit(view=self)

class Leaderboard(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    
  @app_commands.command(name="leaderboard",description='See up to the top 100 members!')
  async def leaderboard(self, interaction: discord.Interaction):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
      # REQUIRED
      extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Leaderboard Command Execute')
      await extra_functions.beforeCommand(self.bot, interaction)
      # DO CODE BELOW
      
      guild_raw = await self.bot.db_pool.fetch('SELECT * FROM user_data WHERE Guild_ID = $1;', interaction.guild_id)
      guild_data = [u for u in guild_raw if len(u['candy_bag']) != 0 and interaction.guild.get_member(u['member_id']) != None]
      members = {}

      index = -1

      i = 0
      for user_data in guild_data:
        members[user_data['member_id']] = len(user_data['candy_bag'])
        i += 1

      sorted_users = sorted(members.items(), key=lambda x: x[1], reverse=True)

      if len(sorted_users) == 0:
        return await interaction.response.send_message(content='Looks like no one has candy yet. Go get some!', ephemeral=True)

      i = 0
      for user_data in sorted_users:
        if user_data[0] == interaction.user.id:
          index = i
        i += 1

      page = 0
      max_page = 9

      if len(sorted_users) <= 90:
        max_page = int((len(sorted_users) - 1) / 10) + 1
        
      string = "```css\n[Rank] | {.Candy.} | Treater\n==========================================\n"

      i = 0
      fucking_eat_my_ass = False
      for user in sorted_users:
        if i >= page * 10:
          try:
            user[0]
          except (IndexError, KeyError, TypeError):
            break

          if(user[0] == interaction.user.id):
              fucking_eat_my_ass = True

          try:
            u = interaction.guild.get_member(user[0])
            if u != None:
                string += " " + "[" + str(i+1).zfill(2) + "]" + "  |   " + str(user[1]).zfill(5) + "   | " + u.display_name[:18] + "\n"
          except Exception as e:
            try:
              u = await interaction.guild.fetch_member(user[0])
              if u != None:
                string += " " + "[" + str(i+1).zfill(2) + "]" + "  |   " + str(user[1]).zfill(5) + "   | " + u.display_name[:18] + "\n"
            except Exception as e:
              self.bot.logger.error(user.id + ' | Leaderboard Member Get Failed')
        
        i += 1

        if i >= page * 10 + 10:
          break

      if not fucking_eat_my_ass:
        if index != -1:
          string += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n " + "[" + str(index+1).zfill(2) + "]" + "  |   " + str(sorted_users[index][1]).zfill(5) + "   | " + interaction.user.display_name[:18] + "\n"
        else:
          string += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n " + "[" + str(interaction.guild.member_count) + "]  |   00000   | " + interaction.user.display_name[:18] + "\n"

      string += '```'
      embed = extra_functions.embedBuilder(interaction.guild.name + "'s Leaderboard",string,"Page 1/" + str(max_page)  + " | Use Arrows to switch pages",0xFF42AE)
      
      view = page_viewer(interaction, sorted_users, index, max_page, interaction.user.id)

      await interaction.response.send_message(embed=embed, view=view)
      view.response = await interaction.original_response()

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Leaderboard(bot))