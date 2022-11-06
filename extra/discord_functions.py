from urllib import response
import discord, random, asyncio, asyncpg, os, os.path, time
from datetime import datetime
from urllib.parse import quote_plus

class PatreonLink(discord.ui.View):
    def __init__(self, label: str, query: str):
        super().__init__()
        # we need to quote the query string to make a valid url. Discord will raise an error if it isn't valid.
        # query = quote_plus(query)
        url = query
        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discord.ui.Button(label=label, url=url))

class extra_functions:

    @staticmethod
    def logger_print(string):
        string = str(string)
        with open('discord_console_logger.txt', encoding='utf-8', mode='a') as f:
            try:
                f.write(str(datetime.now()) + " | " + string + "\n")
            except(TypeError, ValueError,UnicodeDecodeError,OSError,EOFError):
                pass
        print(str(datetime.now())," | ",string)
        return

    @staticmethod
    async def readyCheck(bot, interaction):
        if interaction.guild.chunked == False and not interaction.guild_id in bot.guild_chunk and not interaction.guild.id in bot.chunked:#if bot.ready == False or not interaction.guild_id in bot.ready_guilds:
            bot.guild_chunk.append(interaction.guild_id)
        
        if not interaction.guild.id in bot.chunked:
            try:
                ts = 0
                i = 0
                for x in bot.guild_chunk:
                    i += 1
                    if x == interaction.guild_id:
                        ts = i * 2
                await interaction.response.send_message("Looks like the bot is restarting. This server has been put on a queue to sync! Please wait up to " + str(int(ts/60)) + " minutes, " + str(int(ts+1) % 60) + " seconds!", ephemeral=True)
            except:
                bot.logger.error('Not Chuck Interaction Response Denied')
            return False

        if bot.ready == False:
            try:
                await interaction.response.send_message("Looks like the bot is updating. Try again around 5 seconds!", ephemeral=True)
            except:
                bot.logger.error('Not Ready Interaction Response Denied')
            return False
        return True

    @staticmethod
    async def readyCheckCD(bot, interaction):
        if interaction.guild.chunked == False and not interaction.guild_id in bot.guild_chunk:#if bot.ready == False or not interaction.guild_id in bot.ready_guilds:
            bot.guild_chunk.append(interaction.guild_id)
        
        if interaction.guild.chunked == False:
            return False

        if bot.ready == False:
            return False
        return True

    @staticmethod
    def logUseInfo(bot, user, guild, content):
        bot.logger.info(extra_functions.printGuildUserDetails(guild, user) + ' - ' + content)

    @staticmethod
    def logUseError(bot, user, guild, content):
        bot.logger.info(extra_functions.printGuildUserDetails(guild, user) + ' - ' + content)

    @staticmethod
    async def getPremium(bot, interaction):
        dedicated_json = bot.dedicated_patreon
        dedicated = dedicated_json['premium']

        data = await bot.patreon.fetch('SELECT * FROM existing')
        
        bought_existing = [exist for exist in data if exist['guild_id'] == interaction.guild_id]
        dedicated_existing = [exist for exist in dedicated if exist['guild_id']  == interaction.guild_id]

        if len(bought_existing) == 0 and len(dedicated_existing) == 0:
            return False
        return True

    @staticmethod
    async def checkEmail(bot, email):
        data = await bot.patreon.fetch('SELECT * FROM existing')
        
        bought_existing = [exist for exist in data if exist['email'] == email]

        if len(bought_existing) == 0:
            return False
        return True

    @staticmethod
    async def returnPremiumMessage(bot, interaction):
        if await extra_functions.getPremium(bot, interaction) == False and interaction.user.id != 198305088203128832:
            embed = discord.Embed(title='This is a patreon only feature.', description= '⠀\nLooks like you haven\'t purchased the patreon package! For only **$3** You can use this command and many others along with other servers who have premium as well!. Check out the link for more info especially if you haven\'t purchased it yet.\n⠀')
            embed.set_footer(text='If you have already purchased it, try out /setup_patreon')

            await interaction.response.send_message(embed=embed, view=PatreonLink('Patreon Link', 'https://www.patreon.com/thekwitt'))
            return False
        return True

    @staticmethod
    async def beforeCommand(bot, interaction):
        await bot.db_pool.execute("INSERT INTO guild_settings (Guild_ID) VALUES ($1) ON CONFLICT (Guild_ID) DO NOTHING;", interaction.guild.id)
        await bot.db_pool.execute("INSERT INTO command_cooldowns (Guild_ID) VALUES ($1) ON CONFLICT (Guild_ID) DO NOTHING;", interaction.guild.id)
        await bot.db_pool.execute("INSERT INTO guild_stats (Guild_ID) VALUES ($1) ON CONFLICT (Guild_ID) DO NOTHING;", interaction.guild.id)

        settings = await bot.db_pool.fetchrow('SELECT * FROM guild_settings WHERE Guild_ID = $1', interaction.guild.id)
        if settings['setup'] == True:
            await bot.db_pool.execute("INSERT INTO user_data (Guild_ID, Member_ID) VALUES ($1, $2) ON CONFLICT (Guild_ID, Member_ID) DO NOTHING;", interaction.guild.id, interaction.user.id)
            await bot.db_pool.execute("INSERT INTO user_stats (Guild_ID, Member_ID) VALUES ($1, $2) ON CONFLICT (Guild_ID, Member_ID) DO NOTHING;", interaction.guild.id, interaction.user.id)

    @staticmethod
    async def Insert_User(bot, guild_id, user_id):
        settings = await bot.db_pool.fetchrow('SELECT * FROM guild_settings WHERE Guild_ID = $1', guild_id)
        if settings['setup'] == True:
            await bot.db_pool.execute("INSERT INTO user_data (Guild_ID, Member_ID) VALUES ($1, $2) ON CONFLICT (Guild_ID, Member_ID) DO NOTHING;", guild_id, user_id)
            await bot.db_pool.execute("INSERT INTO user_stats (Guild_ID, Member_ID) VALUES ($1, $2) ON CONFLICT (Guild_ID, Member_ID) DO NOTHING;", guild_id, user_id)
    @staticmethod
    def point_rpg_string(points):
        p_string = str(points)
        if(points > 100000000):
            return p_string[:3] + "." + p_string[3:4] + "M"
        elif(points > 10000000):
            return p_string[:2] + "." + p_string[2:3] + "M"
        elif(points > 1000000):
            return p_string[:1] + "." + p_string[1:3] + "M"
        elif(points > 100000):
            return p_string[:3] + "." + p_string[3:4] + "K"
        elif(points > 10000):
            return p_string[:2] + "." + p_string[2:3] + "K"
        return p_string 

    @staticmethod
    async def setupCheck(bot, guild):
        settings = await bot.db_pool.fetchrow('SELECT * FROM guild_settings WHERE Guild_ID = $1', guild.id)
        if(settings == None or settings['setup'] == False):
            return False
        return True

    @staticmethod
    async def getGuildSettings(bot, guild):
        return await bot.db_pool.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;", guild.id)

    @staticmethod
    def printGuildDetails(guild):
        return guild.name + ' | ' + str(guild.id) + '(' + str(len(guild.members)) + ')'

    @staticmethod
    def printGuildUserDetails(guild, user):
        return guild.name + ' (' + str(guild.id) + ') (' + str(len(guild.members)) + ') | ' + user.name

    @staticmethod
    async def getUserData(bot, guild, user):
        return await bot.db_pool.fetchrow("SELECT * FROM user_data WHERE Guild_ID = $1 AND Member_ID = $2;", guild.id, user.id)

    @staticmethod
    async def reloadMessageDrop(bot, guild):
        try:
            row = await bot.db_pool.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;", guild.id)
            timestamp = row['drop_time_count'] + time.time()
            bot.messages[str(guild.id)] = {'timestamp': timestamp, 'messageCount': row['drop_message_count'], 'activeMessage': False}
            bot.logger.info(str(guild.id) + ' - Guild message was reset!')
        except:
            bot.logger.error(str(guild.id) + ' - Guild message failed to reset!')

    @staticmethod
    async def reloadMessageDropWithoutActive(bot, guild):
        try:
            row = await bot.db_pool.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;", guild.id)
            timestamp = row['drop_time_count'] + time.time()
            bot.messages[str(guild.id)]['timestamp'] = timestamp
            bot.messages[str(guild.id)]['messageCount'] = row['drop_message_count']
            bot.logger.info(str(guild.id) + ' - Guild message was reset Without Active!')
        except:
            bot.logger.error(str(guild.id) + ' - Guild message failed to reset Without Active!')

    @staticmethod
    def logger_noprint(string):
        string = str(string)
        with open('discord_console_logger.txt', encoding='utf-8', mode='a') as f:
            try:
                f.write(str(datetime.now()) + " | " + string + "\n")
            except(TypeError, ValueError,UnicodeDecodeError,OSError,EOFError):
                pass
        return

    @staticmethod
    def tag_to_user(bot,tag):
        return bot.get_user(int(tag.replace('<','').replace('>','').replace('!','').replace('@','')))
        
    @staticmethod
    def user_to_tag(bot,user_id):
        return "<@!" + str(user_id) + ">"

    @staticmethod
    def tag_to_user(bot,tag):
        return bot.get_user(int(tag.replace('<','').replace('>','').replace('!','').replace('@','')))
        
    @staticmethod
    def user_to_tag(bot,user_id):
        return "<@!" + str(user_id) + ">"

    @staticmethod
    def embedBuilder(title,description,footer,color):
        embed = discord.Embed(title = title,description = "⠀\n" + description + "\n⠀",color = color)
        embed.set_footer(text=footer)
        return embed

    @staticmethod
    def embedBuilder_url(title,description,footer,color,url):
        embed = discord.Embed(title = title,description = "⠀\n" + description + "\n⠀",color = color, url=url)
        embed.set_footer(text=footer)
        return embed

    @staticmethod
    def embedBuilder_thumbnail(title,description,footer,color,thumbnail):
        embed = discord.Embed(title = title,description = "⠀\n" + description + "\n⠀",color = color, thumbnail = thumbnail)
        embed.set_footer(text=footer)
        return embed

    @staticmethod
    def embedBuilder_both(title,description,footer,color,url,thumbnail):
        embed = discord.Embed(title = title,description = "⠀\n" + description + "\n⠀",color = color, url = url,thumbnail = thumbnail)
        embed.set_footer(text=footer)
        return embed

    @staticmethod
    async def send_regular_message(bot,content,message,seconds,error_path):
        row = await bot.pg_con.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;",message.guild.id)
        settings = row["default_message_settings"]
        for x in range(0,3):
            try:
                if(settings[3] == "True"):
                    return await message.channel.send(content = content,delete_after=seconds)
                else:
                    return await message.channel.send(content = content)
            except discord.errors.Forbidden:
                extra_functions.logger_print("Forbidden Send occured at " + error_path + " in " + message.guild.name + " | " + str(message.guild.id) + ".")
            except discord.errors.HTTPException as e:
                extra_functions.logger_print(str(e) + " occured at " + error_path + " in " + message.guild.name + " | " + str(message.guild.id) + ".")
    
    @staticmethod
    async def send_regular_channel(bot,content,channel,seconds,error_path):
        row = await bot.pg_con.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;",channel.guild.id)
        settings = row["default_message_settings"]
        for x in range(0,3):
            try:
                if(settings[3] == "True"):
                    return await channel.send(content = content,delete_after=seconds)
                else:
                    return await channel.send(content = content)
            except discord.errors.Forbidden:
                extra_functions.logger_print("Forbidden Send occured at " + error_path + " in " + channel.guild.name + " | " + str(channel.guild.id) + ".")
            except discord.errors.HTTPException as e:
                extra_functions.logger_print(str(e) + " occured at " + error_path + " in " + channel.guild.name + " | " + str(channel.guild.id) + ".")
            
    @staticmethod
    async def send_regular_ctx(bot,content,ctx,seconds,error_path):
        row = await bot.pg_con.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;",ctx.message.guild.id)
        settings = row["default_message_settings"]
        for x in range(0,3):
            try:
                if(settings[3] == "True"):
                    return await ctx.channel.send(content = content,delete_after=seconds)
                else:
                    return await ctx.channel.send(content = content)
            except discord.errors.Forbidden:
                extra_functions.logger_print("Forbidden Send occured at " + error_path + " in " + ctx.guild.name + " | " + str(ctx.guild.id) + ".")
            except discord.errors.HTTPException as e:
                extra_functions.logger_print(str(e) + " occured at " + error_path + " in " + ctx.guild.name + " | " + str(ctx.guild.id) + ".")


    @staticmethod
    async def send_embed_message(bot,message,embed,seconds,error_path):
        row = await bot.pg_con.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;",message.guild.id)
        settings = row["default_message_settings"]
        for x in range(0,3):
            try:
                if(settings[3] == "True"):
                    return await message.channel.send(embed=embed,delete_after=seconds)
                else:
                    return await message.channel.send(embed=embed)
            except discord.errors.Forbidden:
                extra_functions.logger_print("Forbidden Send occured at " + error_path + " in " + message.guild.name + " | " + str(message.guild.id) + ".")
            except discord.errors.HTTPException as e:
                extra_functions.logger_print(str(e) + " occured at " + error_path + " in " + message.guild.name + " | " + str(message.guild.id) + ".")

    @staticmethod
    async def send_embed_ctx(bot,ctx,embed,seconds,error_path):
        row = await bot.pg_con.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;",ctx.guild.id)
        settings = row["default_message_settings"]
        for x in range(0,3):
            try:
                if(settings[3] == "True"):
                    return await ctx.send(embed=embed,delete_after=seconds)
                else:
                    return await ctx.send(embed=embed)
            except discord.errors.Forbidden:
                extra_functions.logger_print("Forbidden Send occured at " + error_path + " in " + ctx.message.guild.name + " | " + str(ctx.message.guild.id) + ".")
            except discord.errors.HTTPException as e:
                extra_functions.logger_print(str(e) + " occured at " + error_path + " in " + ctx.message.guild.name + " | " + str(ctx.message.guild.id) + ".")

    @staticmethod
    def time_to_string(timestamp):
        string = ""
        if(timestamp > 3600):
            if(timestamp/3600 == 1):
                string += "1 Hour, "
            else:
                string += str(int(timestamp/3600)) + " Hours, "

            if(timestamp/60) % 60 == 1:
                string += "1 Minute, "
            else:
                string += str(int((timestamp/60) % 60))  + " Minutes, "

            if timestamp % 60 == 1:
                string += "1 Second, "
            else:
                string += str(timestamp % 60) + " Seconds "
        
        elif(timestamp > 60):
            
            if(timestamp/60) % 60 == 1:
                string += "1 Minute, "
            else:
                string += str(int((timestamp/60) % 60))  + " Minutes, "

            if timestamp % 60 == 1:
                string += "1 Second, "
            else:
                string += str(timestamp % 60) + " Seconds "

        else:
            if timestamp % 60 == 1:
                string += "1 Second, "
            else:
                string += str(timestamp % 60) + " Seconds "
        
        return string

    @staticmethod
    async def send_embed_channel(bot,channel,embed,seconds,error_path):
        row = await bot.pg_con.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;",channel.guild.id)
        settings = row["default_message_settings"]
        try:
            if(settings[3] == "True"):
                return await channel.send(embed=embed,delete_after=seconds)
            else:
                return await channel.send(embed=embed)
        except discord.errors.Forbidden:
            extra_functions.logger_print("Forbidden Send occured at " + error_path + " in " + channel.guild.name + " | " + str(channel.guild.id) + ".")
        except discord.errors.HTTPException as e:
            extra_functions.logger_print(str(e) + " occured at " + error_path + " in " + channel.guild.name + " | " + str(channel.guild.id) + ".")

    @staticmethod
    async def edit_embed_message(bot,message,embed,error_path):
        for x in range(0,3):
            try:
                return await message.edit(embed=embed)
            except discord.errors.Forbidden:
                extra_functions.logger_print("Forbidden Send occured at " + error_path + " in " + message.guild.name + " | " + str(message.guild.id) + ".")
            except discord.errors.HTTPException as e:
                extra_functions.logger_print(str(e) + " occured at " + error_path + " in " + message.guild.name + " | " + str(message.guild.id) + ".")
            except discord.errors.NotFound:
                extra_functions.logger_print("Not Found Send occured at " + error_path + " in " + message.guild.name + " | " + str(message.guild.id) + ".")
            except AttributeError:
                extra_functions.logger_print("Attribute Error occured at " + error_path + " in " + message.guild.name + " | " + str(message.guild.id) + ".")


    @staticmethod
    def str_to_bool(s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            pass#raise ValueError 

    @staticmethod
    def check_for_empty_sql_array(value):
        if(value == None):
            return []
        else:
            return value

    @staticmethod
    async def reset_server_message(bot,guild):
        row = await bot.pg_con.fetchrow("SELECT * FROM guild_settings WHERE Guild_ID = $1;",guild.id)

        active_settings = row["active_message_settings"]
        default_settings = row["default_message_settings"]
        active_settings[0] = int(default_settings[0]) + datetime.now().timestamp()
        active_settings[1] = int(default_settings[1])
        if len(row['possible_channel_ids']) > 0:
            await bot.pg_con.execute("UPDATE guild_settings set active_message_settings = $1,message_state = $2 WHERE Guild_ID = $3;",active_settings,0,guild.id) #Update Loved
        else:
            await bot.pg_con.execute("UPDATE guild_settings set active_message_settings = $1,message_state = $2 WHERE Guild_ID = $3;",active_settings,-1,guild.id) #Update Loved
        await bot.pg_con.execute("DELETE from egg_messages WHERE Guild_ID = $1;",guild.id)
        extra_functions.logger_noprint(guild.name + " : " + str(guild.id) + " - Reset Server Spawn")

    @staticmethod
    async def change_roles(bot, guild):

        temp_role = None
        print('fuck')
        count = 'candy_bag'
        role_name = 'hallow\'s champion'

        for r in guild.roles:
            if role_name in r.name.lower():
                temp_role = r
                break

        if temp_role != None:
            row = await bot.db_pool.fetch("SELECT * FROM user_data WHERE Guild_ID = $1 AND cardinality(candy_bag) != 0 ORDER BY cardinality(candy_bag) DESC", guild.id)
            row = [u for u in row if len(u['candy_bag']) != 0 and guild.get_member(u['member_id']) != None]

            top_users = []
            
            for u in row:
                if (len(row[0][count]) == len(u[count])):
                    #bot.logger.info(str(len(row[0][count])) + ' | ' + str(len(u[count])))
                    member = None
                    try:
                        member = guild.get_member(int(u["member_id"]))
                        top_users.append(u["member_id"])
                    except(IndexError,TypeError):
                        pass
                    if(member != None):
                        if not role_name in [r.name.lower() for r in member.roles]:
                            try:
                                if int(len(u[count])) != 0:
                                    await member.add_roles(temp_role)
                            except:
                                return extra_functions.logUseError(bot,u['member_id'],guild,'Not Member - Add Role')
            for temp in [t for t in temp_role.members if not t.id in top_users]:
                try:
                    await temp.remove_roles(temp_role)
                except:
                    return extra_functions.logUseError(bot,temp,guild,'Not Member - Remove Role')
        else:
            return bot.logger.error(str(guild.id) + ' - No Role')
            
    @staticmethod
    async def check_for_main_channel(guild):
        for c in guild.channels:
            if(isinstance(c,discord.TextChannel)):
                if "general" in c.name or "banter" in c.name or "main" in c.name:
                    return c
    
    @staticmethod
    def bracket_array(type):
        if type == 1:
            return [["<:TL01:825100052976107562>","<:TopLine01:825100053181497394>","<:TR01:825100052782645344>"],["<:BL01:825100053047017563>","<:BottomLine01:825100053068775425>","<:BR01:825100052837040130>"],["<:Empty:825101942644408350>","",""]]
        elif type == 2:
            return [["<:RTL01:825100053071790171>","<:RichTopLine01:825100053143093359>","<:RTR01:825100052535181313>"],["<:RBL01:825100052733100053>","<:RichBottomLine01:825100448233947256>","<:RBR01:825100052824850453>"],["<:Empty:825101942644408350>","",""]]


