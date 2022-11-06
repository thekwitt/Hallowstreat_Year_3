from code import interact
from turtle import undo
import discord, time
from discord import app_commands, Interaction
from discord.ext import commands
from typing import Optional
from discord.app_commands import AppCommandError
from extra.discord_functions import extra_functions

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont,ImageOps

class FireView(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='1',label='Titles List')
  async def fire1(self, interaction: discord.Interaction, button: discord.ui.Button):
    string = 'All titles are based on your collected stat on the card\n\n'
    titles = {'Candy Eater': 0, 'Candy Collector': 100, 'Candy Venturer': 200, 'Candy Adventurer' : 400, 'Candy Mercenary': 600, 'Candy Crusader':1000 , 'Candy Daredevil':1500, 'Candy Hero':2000, 'Candy Knight': 3000, 'Candy Hallower':4000, 'I Am Candy':5000, 'Headless Horseman Arch Rival': 7500, 'The Flash': 10000}
    for title in titles:
        string += title + ' | ' + str(titles[title]) + '\n'
    await interaction.response.send_message(content=string, ephemeral=True,)

class Card(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    
  @app_commands.command(name="card",description='User\'s Profile Card')
  @app_commands.describe(user='The user you want to ')
  async def shitass(self, interaction: discord.Interaction, user: Optional[discord.User]):
    if(await extra_functions.readyCheck(self.bot, interaction) == True):
        # REQUIRED
        extra_functions.logUseInfo(bot=self.bot,user=interaction.user,guild=interaction.guild,content='Card Command Execute')
        if await extra_functions.setupCheck(self.bot, interaction.guild) == False:
            return await interaction.response.send_message("Looks like this bot has not been set up yet. Get a moderator to use **/setup** to get started!", ephemeral=True)
        await extra_functions.beforeCommand(self.bot, interaction)
        titles = {'Candy Eater': 0, 'Candy Collector': 100, 'Candy Venturer': 200, 'Candy Adventurer' : 400, 'Candy Mercenary': 600, 'Candy Crusader':1000 , 'Candy Daredevil':1500, 'Candy Hero':2000, 'Candy Knight': 3000, 'Candy Hallower':4000, 'I Am Candy':5000, 'Headless Horseman Arch Rival': 7500, 'The Flash': 10000}
        # DO CODE BELOW

        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

        u_obj = interaction.user
        if user != None:
            u_obj = user

        if u_obj.bot == True:
            return await interaction.response.send_message(content='Bots don\'t have a card :c')

        if await self.bot.db_pool.fetchrow("SELECT 1 FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", u_obj.id, interaction.guild_id) == None:
            await extra_functions.Insert_User(self.bot,interaction.guild.id,u_obj.id)   

        user_data = await self.bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Member_ID = $1 AND Guild_ID = $2", u_obj.id, interaction.guild_id)

        asset = u_obj.display_avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp_base = Image.open(data).resize((134,134))

        size = (134, 134)
        mask = Image.new('L', size, 0)

        outline = (237,203,135,255)

        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + size, fill=255)

        pfp = ImageOps.fit(pfp_base, mask.size, centering=(0.5, 0.5))
        pfp.putalpha(mask)
        pfp = pfp.convert("RGBA")


        base = Image.open("Card/Card.png").convert("RGBA") #template
        text = Image.new("RGBA", base.size, (255,255,255,0)) #blank image for text

        base.paste(pfp_base.convert("RGBA"), (30,30), pfp.convert("RGBA"))

        t_font = ImageFont.truetype("Card/Title.ttf",60) # Title Font
        r_font = ImageFont.truetype("Card/Rank.ttf",36) # Rank Font
        p_font = ImageFont.truetype("Card/Points.ttf",48) # Point Font
        c_font = ImageFont.truetype("Card/Count.ttf",60) # Point Font
        #l_font = ImageFont.truetype("Card/LB.ttf",60) # Rank Font
        d_text = ImageDraw.Draw(text) # Draw Text Image

        largest_title = None
        for title in titles:
            bag = user_data['candy_collected']
            if bag >= titles[title]:
                largest_title = title
            else:
                break
      
        guild_raw = await self.bot.db_pool.fetch('SELECT * FROM user_data WHERE Guild_ID = $1;', interaction.guild_id)
        guild_pre = [u for u in guild_raw if len(u['candy_bag']) != 0 and interaction.guild.get_member(u['member_id']) != None]
        user_place = 0
        user_ranked = False

        guild_data = sorted(guild_pre, key=lambda x: len(x['candy_bag']), reverse=True)

        for u in guild_data:
            if u['member_id'] == u_obj.id:
                user_ranked = True
                break
            user_place += 1


        d_text.text((195,35),u_obj.display_name[:18],font=t_font,fill=(0,0,0,255), stroke_width=2, stroke_fill=(0,0,0,100))
        d_text.text((190,30),u_obj.display_name[:18],font=t_font,fill=(237,174,92,255), stroke_width=2, stroke_fill=(0,0,0,100))
        d_text.text((193,108),largest_title,font=r_font,fill=(0,0,0,255), stroke_width=2, stroke_fill=(0,0,0,100))  
        d_text.text((190,105),largest_title,font=r_font,fill=(240,197,141,255), stroke_width=2, stroke_fill=(0,0,0,100))  
        d_text.text((35,289),"Candy Bag - " + extra_functions.point_rpg_string(len(user_data['candy_bag'])),font=p_font,fill=(242,213,174,255), stroke_width=2, stroke_fill=(0,0,0,255))
        d_text.text((35,359),"Collected - " + str(extra_functions.point_rpg_string(user_data['candy_collected'])),font=p_font,fill=(245,199,140,255), stroke_width=2, stroke_fill=(0,0,0,255))
        d_text.text((35,429),"Collection - " + str(extra_functions.point_rpg_string(len(user_data['candy_completion'])) + '/' + str(len(self.bot.candy))),font=p_font,fill=(242,147,22,255), stroke_width=2, stroke_fill=(0,0,0,255))
        if user_ranked == True:
            d_text.text((1170,470),"Rank - " + ordinal(user_place + 1),font=c_font,fill=(237,177,97,255), stroke_width=3, stroke_fill=(0,0,0,255), anchor='rs')
        else:
            d_text.text((1170,470),"Unranked",font=c_font,fill=(237,177,97,255), stroke_width=3, stroke_fill=(0,0,0,255), anchor='rs')
        
        if user_data['eat_bonus'] != -1:
           d_text.text((33,206),'Bonus - ' + ['Collector Mask','Second Wind','Backstab','Mental Shield','The Ugly','Power Up','Golden Collector Mask','Golden Second Wind','Golden Backstab','Golden Mental Shield','The Golden Ugly','Golden Power Up'][user_data['eat_bonus']] + ' | ' + str(int((user_data['eat_expire']-time.time())/60)) + ' Minutes Left',font=r_font,fill=(181,82,20,255), stroke_width=2, stroke_fill=(0,0,0,255))
           d_text.text((30,203),'Bonus - ' + ['Collector Mask','Second Wind','Backstab','Mental Shield','The Ugly','Power Up','Golden Collector Mask','Golden Second Wind','Golden Backstab','Golden Mental Shield','The Golden Ugly','Golden Power Up'][user_data['eat_bonus']] + ' | ' + str(int((user_data['eat_expire']-time.time())/60)) + ' Minutes Left',font=r_font,fill=(245,193,162,255), stroke_width=2, stroke_fill=(0,0,0,255))

        out = Image.alpha_composite(base,text)

        with BytesIO() as image_binary:
            out.save(image_binary,'PNG')
            image_binary.seek(0)
            try:
                await interaction.response.send_message(file=discord.File(fp=image_binary, filename='image.png'),view=FireView())
            except discord.errors.Forbidden:
                extra_functions.logUseError(self.bot, u_obj, "Forbidden Send occured at eggard self")
            except discord.errors.HTTPException:
                extra_functions.logger_print(self.bot, u_obj, "HTTP Error Send occured at eggard self")


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Card(bot))