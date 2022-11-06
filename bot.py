import discord, asyncpg, os.path, logging, logging.handlers, json, asyncio, time, topgg, random, math
from glob2 import glob
from discord.ext.tasks import loop
from typing import List
from discord.ext import commands
from aiohttp import ClientSession
from extra.candySpawner import SpawnCandy
from extra.bossSpawnerHard import SpawnBoss
from extra.discord_functions import extra_functions

TOKENS = json.load(open('./JSON/token.json'))

class BotClient(commands.AutoShardedBot):
    @loop(seconds=3600)
    async def reload_chunking(self):
        if self.ready == True:
            self.chunked = []
            self.guild_chunk = []

    @loop(seconds=60)
    async def expire_checker(self):
        if self.ready == True:
            await self.db_pool.execute('UPDATE user_data SET eat_bonus = -1, eat_notify = TRUE WHERE eat_expire < $1 AND eat_bonus != -1;', time.time())

    @loop(seconds=60)
    async def vc_checker(self):
        for guild in self.guilds:
            try:
                if self.ready == True and guild != None and guild.chunked == True and await extra_functions.setupCheck(self, guild) == True:
                    settings = await extra_functions.getGuildSettings(self, guild)

                    if settings != None:
                        if settings['vc_counter_enable'] == True:
                            if not str(guild.id) in list(self.messages.keys()):
                                return await extra_functions.reloadMessageDrop(bot=self, guild=guild)
                            
                            count = 0
                            for vc in guild.voice_channels:
                                count += len(vc.members)

                            if count != 0:
                                if self.messages[str(guild.id)]['messageCount'] <= 0:
                                    self.logger.info(extra_functions.printGuildDetails(guild) + ' - Already Over')
                                else:
                                    if self.messages[str(guild.id)]['messageCount'] >= 0:
                                        if count < settings['vc_member_count'] * 2:
                                            self.messages[str(guild.id)]['messageCount'] -= 1
                                            self.logger.info(extra_functions.printGuildDetails(guild) + ' - ' + str(self.messages[str(guild.id)]['messageCount']) + ' Left')
                                        else:
                                            self.messages[str(guild.id)]['messageCount'] -= math.floor(count / settings['vc_member_count'])
                                            self.logger.info(extra_functions.printGuildDetails(guild) + ' - ' + str(self.messages[str(guild.id)]['messageCount']) + ' Left')

                                        messageSpawn = self.messages[str(guild.id)]
                                        if messageSpawn['timestamp'] < time.time() and messageSpawn['messageCount'] <= 1 and messageSpawn['activeMessage'] == False:
                                            try:
                                                settings = await extra_functions.getGuildSettings(self, guild)
                                                rand = random.randint(0,100)
                                                if settings['boss_spawn_ratio'] >= rand:
                                                    await SpawnBoss.spawnBossVC(bot=self,guild=guild)
                                                else:
                                                    await SpawnCandy.spawnCandyVC(bot=self,guild=guild)
                                                self.logger.info(extra_functions.printGuildDetails(guild) + ' - VC Sent Event')
                                            except Exception as e:
                                                self.logger(await extra_functions.printGuildDetails(guild) + ' | VC Event Fail | ' + str(e))
                                                return await extra_functions.reloadMessageDrop(bot=self, guild=guild)

            except Exception as e:
                self.logger.error(extra_functions.printGuildDetails(guild) + ' - VC Error: ' + str(e) )



    @loop(seconds=2)
    async def chuck_queue(self):
        if self.ready == True:
            if len(self.guild_chunk) != 0:
                guild = self.get_guild(self.guild_chunk[0])
                if guild == None:
                  self.logger.error(str(self.guild_chunk[0]) + ' failed to chunk.')
                  return self.guild_chunk.remove(self.guild_chunk[0])
                
                if guild.id in self.chunked:
                  self.logger.error(str(self.guild_chunk[0]) + ' already chunked 2.')
                  return self.guild_chunk.remove(self.guild_chunk[0])
                
                if guild.chunked == True:
                  self.logger.error(str(self.guild_chunk[0]) + ' already chunked.')
                  return self.guild_chunk.remove(self.guild_chunk[0])
                  
                try:
                  await guild.chunk()
                  self.chunked.append(guild.id)
                except:
                   self.logger.error(str(self.logger.error(str(self.guild_chunk[0]) + ' failed to chunk 2.')))
                   return self.guild_chunk.remove(self.guild_chunk[0])
                  
                self.guild_chunk.remove(self.guild_chunk[0])
                self.logger.info(extra_functions.printGuildDetails(guild) + ' - Guild Chunked!')



    @loop(seconds=60)
    async def change_presense(self):
        if self.ready:
            sum = await self.db_pool.fetch("SELECT SUM(candy_collected) as total FROM user_data;")
            if random.randint(0, 100) > 50:
                await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= str(len(self.guilds)) + ' servers collect ' + str(extra_functions.point_rpg_string(int(sum[0]['total']))) + ' candy!'))
            else:
                count = 0
                for g in self.guilds:
                    count += g.member_count
                await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= str(extra_functions.point_rpg_string(count)) + ' members collect ' + str(extra_functions.point_rpg_string(int(sum[0]['total']))) + ' candy!'))


    @loop(minutes=30)
    async def update_stats(self):
        try:
            await self.topggpy.post_guild_count()
            self.logger.info(f"Posted server count ({self.topggpy.guild_count})")
        except Exception as e:
            self.logger.error(f"Failed to post server count\n{e.__class__.__name__}: {e}")

    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        db_pool: asyncpg.Pool,
        patreon: asyncpg.Pool,
        vote_log: asyncpg.Pool,
        web_client: ClientSession,
        logger,
        **kwargs,
    ):
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        intents.guilds = True
        intents.members = True
        intents.messages = True
        super().__init__(command_prefix = commands.when_mentioned, intents=intents, chunk_guilds_at_startup=False)
        self.logger = logger
        self.db_pool = db_pool
        self.patreon = patreon
        self.guild_chunk = []
        self.chunked = []
        self.vote_log = vote_log
        self.messages = {}
        self.ready = False
        self.web_client = web_client
        self.dedicated_patreon = json.load(open('./JSON/premium.json'))
        c = json.load(open('./JSON/candy.json'))
        self.candy = [ca for ca in c['candy'] if ca['type'] != '']
        #self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            try:
                await self.load_extension(f"cogs.{extension}")
                self.logger.info(str(extension) + ' cogged')
            except Exception as e:
                try:
                    await self.load_extension(f"cogs.{extension[7:]}")
                    self.logger.info(str(extension) + ' cogged')
                except Exception as e:
                    self.logger.error(str(extension) + ' not cogged\n' + str(e))

        #await self.tree.sync(guild=discord.Object(id = 451929862794641409))
        await self.db_pool.execute(
        """ 
        CREATE TABLE IF NOT EXISTS guild_settings(
            Guild_ID bigint PRIMARY KEY,
            Channel_ID bigint[] DEFAULT '{}',
            Champion_Role_ID bigint DEFAULT 0,
            Drop_Message_Count INTEGER DEFAULT 10,
            Drop_Time_Count INTEGER DEFAULT 300,
            Drop_Duration INTEGER DEFAULT 60,
            Setup BOOLEAN DEFAULT FALSE,
            Delete_OT BOOLEAN DEFAULT FALSE,
            Boss_Difficulty INTEGER DEFAULT 1,
            Boss_Spawn_Ratio INTEGER DEFAULT 30,
            Enable_Giving BOOLEAN DEFAULT TRUE,
            Enable_Scare BOOLEAN DEFAULT TRUE,
            Enable_Trading BOOLEAN DEFAULT TRUE,
            Candy_Object_Per_Drop INTEGER DEFAULT 3,
            Candy_Obtain_Amount INTEGER DEFAULT 3,
            Candy_Steal_Percent INTEGER DEFAULT 5
        );

        CREATE TABLE IF NOT EXISTS command_cooldowns(
            Guild_ID bigint PRIMARY KEY,
            Give INTEGER DEFAULT 1,
            Bulk_Give INTEGER DEFAULT 1,
            Scare INTEGER DEFAULT 15
            );

        CREATE TABLE IF NOT EXISTS user_data(
            Guild_ID bigint,
            Member_ID bigint,
            Eat_Bonus INTEGER DEFAULT -1,
            Eat_Notify BOOLEAN DEFAULT FALSE,
            Eat_Expire bigint DEFAULT 0,
            Candy_Collected INTEGER DEFAULT 0,
            First_Time BOOLEAN DEFAULT FALSE,
            Bot_Update BOOLEAN DEFAULT FALSE,
            Candy_Bag INTEGER[] DEFAULT '{}',
            Candy_Completion INTEGER[] DEFAULT '{}',
            PRIMARY KEY (Guild_ID, Member_ID)
            );

        CREATE TABLE IF NOT EXISTS guild_stats(
            Guild_ID bigint PRIMARY KEY,
            Drops_Spawned INTEGER DEFAULT 0,
            Drops_Collected INTEGER DEFAULT 0,
            Bosses_Spawned INTEGER DEFAULT 0,
            Candy_Collected INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS user_stats(
            Guild_ID bigint,
            Member_ID bigint,
            Candy_Collected INTEGER DEFAULT 0,
            Boss_Defeated INTEGER DEFAULT 0,
            People_Scared INTEGER DEFAULT 0,
            Trades_Completed INTEGER DEFAULT 0,
            Candy_Given INTEGER DEFAULT 0,
            Candy_Stolen INTEGER DEFAULT 0,
            PRIMARY KEY (Guild_ID, Member_ID)
            );
        """
        )
        self.vc_checker.start()
        self.chuck_queue.start()
        self.expire_checker.start()
        self.change_presense.start()
        self.reload_chunking.start()

async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    async with ClientSession() as our_client, asyncpg.create_pool(database = "halloween",user=TOKENS['poolUser'],password=TOKENS['poolPW']) as pool, asyncpg.create_pool(database = "patreon",user=TOKENS['poolUser'],password=TOKENS['poolPW']) as patreon, asyncpg.create_pool(database = "vote_log",user=TOKENS['poolUser'],password=TOKENS['poolPW']) as vote_log:

        async with BotClient(commands.when_mentioned, db_pool=pool, patreon=patreon, vote_log=vote_log, web_client=our_client, initial_extensions= [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")], logger=logger) as bot:
            bot.topggpy = topgg.DBLClient(bot, TOKENS['topgg'])
            bot.update_stats.start()
            await bot.start(TOKENS['token'])

asyncio.run(main())