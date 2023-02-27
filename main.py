#import env variables
import os
from dotenv import load_dotenv
load_dotenv()
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

#import discord bot API
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context

#import rest
import datetime
import pytz
import random

#class for initial bot setup
class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix = "!", intents = intents)

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral = True)    

client = Client() #bot initialisation 

#runs on start
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}.")

#message command to sync slash commands
@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context):
    synced = await client.tree.sync(guild = discord.Object(GUILD_ID))
    print(f"Synced {synced} slash command(s) for {client.user}.")

#scripted_text
scripted_text = list(['You should try out mah pizzahhh! iz good', 'you call it a pizzzahh i call it a work of michelangelo. and im the one that made it', 'they tell me you gonna be something one day well. ohh madone.', 'my wife marie makes the best cupcakes', 'you ever tasted a pizzzah from detroit? no wonder', 'God with a capital G, wiseguy', 'ohh madone.','what you call a doctor with three heads? probably by his name', 'there were three of them. a cheerleader, a broad with an expiry date of three yeasz, and my nephew who dont hear too good. who u pickin to make the best pizza in the penn? ME.', 'you know who make the best pizza in the penn dont yous', 'you ever heard of a machine who pics up all the rotten apples off the dirt? yeah me neither', 'whats new jersey got tah do with it', 'only one of us is making it out and im the best pizza maker in the penn', 'you ever seen heat 1995 film yeah itzza my favorite.', 'dont ever take gods name in vain', 'a chessboard with two kings. you call that a stalemate. i call that a good time', 'you want to hear three jokes well its only a matter of time before they call you up on stage', 'i coulda been a contender', 'you ever been to a lodge near the ocean yeah my great great great grandparents had one in napoli'])

#hybrid command to check and send the number of sleeps until christmas
@client.hybrid_command(name = "christmas_sleeps", with_app_command = True, descrption = "Provides the number of sleeps until Christmas")
@app_commands.guilds(discord.Object(GUILD_ID))
async def christmas_sleeps(ctx: Context):
    timezone = pytz.timezone('Australia/Melbourne')

    christmas_day = datetime.datetime(2023, 12, 25, 7, 0, 0, 0, timezone)
    current_time = datetime.datetime.now(timezone)

    time_diff = christmas_day - current_time
    sleeps = time_diff.days

    if current_time.hour >= 18:
        sleeps -= 1

    random_int = random.randint(0,len(scripted_text)-1)
    chosen_text = scripted_text[random_int]

    user = ctx.author
    await ctx.reply(f"{user.mention} There are {sleeps} sleeps until Christmas day. {chosen_text}")

client.run(CLIENT_TOKEN) #run with token