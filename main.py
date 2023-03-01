#import env variables. use a .env file
import os
from dotenv import load_dotenv
load_dotenv()
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN') #string input
GUILD_ID = int(os.getenv('GUILD_ID')) #integer input
XENON = int(os.getenv('XENON')) #integer input
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

#@client.event
#async def on_message(message):
        #if message.author == client.user:
         #    return 

        #if message.author.id == XENON:
         #   await message.channel.send('Haha?')


#@client.tree.command(name = "gpt", description = "prompt ChatGPT")
@client.command()
@app_commands.guilds(discord.Object(GUILD_ID))
async def gpt(ctx: Context, *, prompt: str):
    async with aiohttp.ClientSession() as session:
        payload = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "temperature": 0.5,
            "max_tokens": 50,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "best_of": 1,
        }
        headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
        async with session.post("https://api.openai.com/v1/completions", json=payload, headers = headers) as resp:
            response = await resp.json()
            embed = discord.Embed(title="GPT:", description=response["choices"][0]["text"])
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

#scripted_text
scripted_text = list(['usedtah have a buddie down in baltimore he never heard of an pork roll egg n cheese. wiseguy.','my daughtah cindy got a new boyfriend. maddonee.','it could never take you five minutes to cook your grits, it takes the entire grit-eating world 20 minutes.','nothing will topa good pizzzah with led zep playing at the maddie square','You should try out mah pizzahhh! iz good', 'you call it a pizzzahh i call it a work of michelangelo. and im the one that made it', 'they tell me you gonna be something one day well. ohh madone.', 'my wife marie makes the best cupcakes','you need a sitdown my friend','you ever tasted a pizzzah from detroit? no wonder', 'God with a capital G, wiseguy', 'ohh madone.','what you call a doctor with three heads? probably by his name', 'there were three of them. a cheerleader, a broad with an expiry date of three yeasz, and my nephew who dont hear too good. who u pickin to make the best pizza in the penn? ME.', 'you know who make the best pizza in the penn dont yous', 'you ever heard of a machine who pics up all the rotten apples off the dirt? yeah me neither', 'whats new jersey got tah do with it', 'only one of us is making it out and im the best pizza maker in the penn', 'you ever seen heat 1995 film yeah itzza my favorite.', 'dont ever take gods name in vain', 'a chessboard with two kings. you call that a stalemate. i call that a good time', 'you want to hear three jokes well its only a matter of time before they call you up on stage', 'i coulda been a contender', 'you ever been to a lodge near the ocean yeah my great great great grandparents had one in napoli'])

#Provides the number of sleeps until a certain few special days. Requires timezone input
@client.tree.command(name = "sleeps_to_holiday", description = "Provides the number of sleeps until a certain few special days. Requires timezone input")
@app_commands.guilds(discord.Object(GUILD_ID))
async def sleeps_to_holiday(interaction: discord.Interaction, chosen_holiday: str, chosen_timezone: str):
    timezone = pytz.timezone(chosen_timezone)
    
    current_time = datetime.datetime.now(timezone)
    timezone_name = current_time.tzname()

    special_day = datetime.datetime.fromisoformat(chosen_holiday)
    #christmas_day_aware = christmas_day.replace(tzinfo=timezone.timezone_name)
    special_day_aware = timezone.localize(special_day)

    time_diff = special_day_aware - current_time
    sleeps = time_diff.days

    if current_time.hour >= 18:
        sleeps -= 1

    holiday_name = None
    if chosen_holiday == '2023-12-25T07:00:00':
        holiday_name = 'normal Christmas'
    if chosen_holiday == '2024-01-07T07:00:00':
        holiday_name = 'Serbian Christmas'
    if chosen_holiday == '2023-11-12T07:00:00':
        holiday_name = 'National Pizza With Everything (Except Anchovies)'


    random_int = random.randint(0,len(scripted_text)-1)
    chosen_text = scripted_text[random_int]

    await interaction.response.send_message(f"{chosen_text} {interaction.user.mention} that's how i know there are {sleeps} sleeps until {holiday_name} day in the timezone region of {timezone} ({timezone_name}).")

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