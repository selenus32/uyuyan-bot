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

    user = ctx.author
    await ctx.reply(f"{user.mention} There are {sleeps} sleeps until Christmas day. You should try out mah pizzahhh! iz good")

client.run(CLIENT_TOKEN) #run with token