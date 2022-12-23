# ================================================================
# IMPORT [os - Miscellaneous operating system interfaces]
import os

# IMPORT [json - config.json]
import json

JSON_FILE = ""
with open('arq/config.json', 'r') as json_file:
	data = json.loads(json_file.read())
	JSON_FILE = data

# IMPORT [pip install discord.py]
import discord
from discord import Embed
from discord.ext import commands
from mandaTrue import on_TrulyFunction


# ================================================================
# CONFIGURE [Discord]
intents = discord.Intents.all()
discord.Intents.members = True
discord.Intents.messages = True
discord.Intents.message_content = True
bot_spright = discord.Client(command_prefix="/", intents=intents)
# variavél [from discord.ext import commands]
bot_spright = commands.Bot(command_prefix="/", intents=intents)

CHANNEL_ID = JSON_FILE['CHANNEL_ID']
channel = bot_spright.get_channel(CHANNEL_ID)
TOKEN = JSON_FILE['TOKEN']

# ================================================================
# APPLICATION [BOT FUNCTIONS]
@bot_spright.event
async def on_ready():
	letSet = f"\033[47m {bot_spright.user} \033[m"
	statusSucess = "\033[46m Conexão Establecida \033[m" #Cyan Background
	newSetSucess = f"\033[1m{statusSucess}\033[m"
	print(f"{letSet}{newSetSucess}")
	print(f"""
		BIBIRUUUUU!! I AM {bot_spright.user}!

		+ Command to exit the application:
		| Press 'Ctrl + C'
		+-+---------------- x ----------------
	""")
	"""
		'r'  -> Usado somente para ler algo;
		'r+' -> Usado para LER e ESCREVER algo;
		'w'  -> Usado somente para escrever algo;
		'w+' -> escrita (o modo w+, assim como o w, também apaga o conteúdo anterior do arquivo);
		'a'  -> Usado para acrescentar algo;
		'a+' -> leitura e escrita (abre o arquivo para atualização)
	"""

# ================================================================
# CONFIGURE [ACTIVE]
@bot_spright.command(name='greet')
async def on_message(message):
	'''
		Greeting message from the bot.
		|
		|
		`--> channel : Channel where the bot will be directed.
			`--> message.channel : Exact channel where the command was performed.
	'''
	channel = message.channel
	user_set = f"<@{message.author.id}>"
	if user_set == "<@303321235679477760>":
		await channel.send(f'Hello, {user_set}! MY FATHER :heart:!!!')
	else:
		await channel.send(f'Hello, {user_set}!')

# ================================================================
# CONFIGURE [PRANKS]
@bot_spright.command(name="mandaTrue")
async def on_Truly(message):
	'''
		Spright Blue will send a fact statement
		(nothing he says should be taken seriously, the robot's purpose being just for fun)
		|
		|
		`--> list_true : List with the listed lines of the bot.
		`--> channel : Channel where the bot will be directed.
			`--> message.channel : Exact channel where the command was performed.
	'''
	channel = message.channel
	list_choice = on_TrulyFunction()
	await channel.send(f'`{list_choice}`')

# ================================================================
# CONFIGURE [WEBHOOK - EMBED]
@bot_spright.command(name='info')
async def on_Embed(message):
    URL_WEBHOOK = JSON_FILE['URL_WEBHOOK']
    DESCRIPTION_EMBED = f"_Bot Spright activated successfully!_{os.linesep}\n\n:computer: **My Creator**{os.linesep}_GitHub_:  https://github.com/Baku-Stark{os.linesep}\n:computer: **Repository**{os.linesep}_GitHub_: https://github.com/Baku-Stark/Spright-Blue"

    embed = Embed(
        url=URL_WEBHOOK,
        title="★ Spright Blue",
        description=DESCRIPTION_EMBED,
        color= discord.Colour.dark_blue()
    ).set_footer(text="Level 2 ★").set_thumbnail(url="https://media.discordapp.net/attachments/1055607254465908877/1055607254700793896/SprightBlue-Icon.png")

    channel = message.channel
    await channel.send(embed=embed)

# ================================================================
# CONFIGURE [run]
bot_spright.run(TOKEN)