#import env variables. use a .env file
import os
from dotenv import load_dotenv
load_dotenv()
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN') #string input
GUILD_ID = int(os.getenv('GUILD_ID')) #integer input
XENON = int(os.getenv('XENON')) #integer input
OWNER_ID = int(os.getenv('OWNER_ID')) #integer input
OPENAI_KEY = os.getenv('OPENAI_KEY')

#import discord bot API
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from typing import List

#import rest
import ety
import aiohttp
import datetime
import pytz
import random
import openai

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

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#       return 
#
#    if message.author.id == XENON:
#       await message.channel.send('')


#message command to sync slash commands
@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context):
    synced = await client.tree.sync(guild = discord.Object(GUILD_ID))
    print(f"Synced {synced} slash command(s) for {client.user}.")

childlock = 0

def not_banned(ctx):
    return ctx.author.id != XENON

@client.command()
@commands.guild_only()
@commands.is_owner()
async def childlock(ctx: Context, boolean: str):
    global childlock
    if boolean.lower() == 'true':
        childlock = 1
        await ctx.reply('Child-lock activated.')
    if boolean.lower() == 'false':
        childlock = 0
        await ctx.reply('Child-lock deactivated.')
    return childlock

@client.command()
@app_commands.guilds(discord.Object(GUILD_ID))
@commands.check(lambda ctx: not childlock or ctx.author.id == OWNER_ID)
@commands.check(not_banned)
async def dalle(ctx: Context, *, prompt: str):
    openai.api_key = OPENAI_KEY
    response = openai.Image.create(prompt=prompt,n=1,size="512x512")
    image_url = response['data'][0]['url']
    embed = discord.Embed(title="DALLE:", description=prompt)
    print(image_url)
    embed.set_image(url=image_url)
    await ctx.reply(embed=embed)

@client.command()
@app_commands.guilds(discord.Object(GUILD_ID))
@commands.check(lambda ctx: not childlock or ctx.author.id == OWNER_ID)
@commands.check(not_banned)
async def gpt(ctx: Context, *, prompt: str):
    openai.api_key = OPENAI_KEY
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens=100,
    messages=[
        {"role": "user", "content": prompt}
    ])
    
    embed = discord.Embed(title="gpt-3.5-turbo:", description=completion.choices[0].message.content)
    await ctx.reply(embed=embed)

#etymology tree for given word
@client.tree.command(name = "ety_tree", description = "Show etymology tree of a given word")
@app_commands.guilds(discord.Object(GUILD_ID))
async def ety_tree(interaction: discord.Interaction, given_word: str):
    embed = discord.Embed(title=f"Etymology tree of {given_word}", description=f"{ety.tree(given_word)}")
    await interaction.response.send_message(embed=embed)

#word origins for given word
@client.tree.command(name = "ety_origins", description = "Show word origin(s) of a given word")
@app_commands.guilds(discord.Object(GUILD_ID))
async def ety_tree(interaction: discord.Interaction, given_word: str):
    embed = discord.Embed(title=f"Word origin(s) of {given_word}", description=f"{ety.origins(given_word, recursive=True)}")
    await interaction.response.send_message(embed=embed)

#Provides the number of sleeps until a certain few special days. Requires timezone input
@client.tree.command(name = "sleeps_to_holiday", description = "Provides the number of sleeps until a certain few special days. Requires timezone input")
@app_commands.guilds(discord.Object(GUILD_ID))
async def sleeps_to_holiday(interaction: discord.Interaction, chosen_holiday: str, chosen_timezone: str):
    timezone = pytz.timezone(chosen_timezone)
    
    current_time = datetime.datetime.now(timezone)
    timezone_name = current_time.tzname()

    special_day = datetime.datetime.fromisoformat(chosen_holiday)
    special_day_aware = timezone.localize(special_day)

    time_diff = special_day_aware - current_time
    sleeps = time_diff.days

    if current_time.hour >= 18:
        sleeps -= 1

    holiday_name = None
    if chosen_holiday == '2023-12-25T07:00:00':
        holiday_name = 'normal Christmas day'
    if chosen_holiday == '2024-01-07T07:00:00':
        holiday_name = 'Serbian Christmas day'
    if chosen_holiday == '2023-11-12T07:00:00':
        holiday_name = 'National Pizza With Everything (Except Anchovies) day'

    embed = discord.Embed(title=f"Orrrhooo orrrhooo", description=f"{interaction.user.mention} there are {sleeps} sleeps until {holiday_name} in the timezone region of {timezone} ({timezone_name}).")
    await interaction.response.send_message(embed=embed)

#defines choices in previous function
@sleeps_to_holiday.autocomplete("chosen_timezone")
async def sleeps_to_holiday_timezone_autocompletion(
    interaction: discord.Interaction, 
    current: str
    ) -> List[app_commands.Choice[str]]:
        picked_timezones = ['Africa/Dakar','Africa/Lagos','Africa/Tunis','Africa/Gaborone','America/Anchorage','America/Edmonton','America/Detroit','America/Halifax','America/Campo_Grande','America/Merida','America/Mexico_City','America/Porto_Acre','Antarctica/South_Pole','Asia/Tbilisi','Asia/Sakhalin','Asia/Samarkand','Asia/Ulaanbaatar','Atlantic/Jan_Mayen','Australia/Melbourne','Australia/Brisbane','Europe/Zaporozhye','Europe/Isle_of_Man','Europe/Belgrade','Europe/Astrakhan','Indian/Christmas']
        data = []
        for timezone_choice in picked_timezones:
            data.append(app_commands.Choice(name=timezone_choice, value = timezone_choice))
        return data

@sleeps_to_holiday.autocomplete("chosen_holiday")
async def chosen_holiday_autocompletion(
    interaction: discord.Interaction, 
    current: str
    ) -> List[app_commands.Choice]:
        data = []
        data.append(app_commands.Choice(name='Normal Christmas', value ='2023-12-25T07:00:00'))
        data.append(app_commands.Choice(name='Serbian Christmas', value ='2024-01-07T07:00:00'))
        data.append(app_commands.Choice(name='National Pizza With Everything (Except Anchovies) Day', value='2023-11-12T07:00:00'))
        return data

client.run(CLIENT_TOKEN) #run with token