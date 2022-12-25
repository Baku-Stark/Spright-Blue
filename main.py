# ================================================================
# IMPORT [os - Miscellaneous operating system interfaces]
import os

# IMPORT [wavelink]
import wavelink

# IMPORT [json - config.json]
import json

JSON_FILE = ""
with open('arq/config.json', 'r') as json_file:
	'''
		'r'  -> Usado somente para ler algo;
		'r+' -> Usado para LER e ESCREVER algo;
		'w'  -> Usado somente para escrever algo;
		'w+' -> escrita (o modo w+, assim como o w, também apaga o conteúdo anterior do arquivo);
		'a'  -> Usado para acrescentar algo;
		'a+' -> leitura e escrita (abre o arquivo para atualização)
	'''
	data = json.loads(json_file.read())
	JSON_FILE = data

# IMPORT [pip install discord.py]
import discord
from discord import Embed
from discord.ext import commands

# IMPORT [datetime - calendar]
from datetime import datetime
update_times = datetime.strftime(datetime.now(),'20%y/%m/%d [%I:%M]')

# IMPORT [rich - dashboard(console)]
from rich import print
from rich.tree import Tree
from rich.panel import Panel

# IMPORT [mandaTrue.py > on_TrulyFunction]
from mandaTrue import on_TrulyFunction

# IMPORT [function > files]
from function.connection import connection_test

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
# APPLICATION [Main Function ACTIVE]
class CustomPlayer(wavelink.Player):
	def __init__(self):
		super().__init__()
		self.queue = wavelink.Queue()

@bot_spright.event
async def on_ready():
	'''
		Bot activation check.
		|
		|
		`--> Panel.fit : Operation message successfully activated.
			`--> bot_spright.user : Return user's bot Spright Blue.
			`--> tree : Main command tree.
	'''
	# Connection Test
	print(connection_test())

	# HTTPS and websocket operations
	bot_spright.loop.create_task(connect_nodes())

	# Panel Greeting
	print(Panel.fit(f"[bold blue]Hi, human!!!\nI am {bot_spright.user}", border_style="cyan", title="Bot Discord"))

	# Tree Commands
	tree = Tree("[bold white]Command to exit the application")
	tree.add("command : Press [cyan]'Ctrl + C'[/cyan]")
	print(tree)

# ================================================================
# CONFIGURE [MUSIC]
async def connect_nodes():
	await bot_spright.wait_until_ready()
	
	await wavelink.NodePool.create_node(
		bot=bot_spright,
		host='0.0.0.0',
		port=2333,
		password='youshallnotpass'
	)

@bot_spright.command(name='play')
async def joinChannel(msg, urlYT: str):
	user_set = f"<@{msg.author.id}>"
	if not msg.message.author.voice:
		await msg.reply(f"Entre em alguma sala, {user_set}")
		return

	else:
		# mostra o canal de voz onde o user está
		voiceChannel = discord.utils.get(msg.guild.voice_channels, name=f'{msg.message.author.voice.channel}')
		await msg.reply(urlYT)
		await voiceChannel.connect()

@bot_spright.command(name='leave')
async def leaveChannel(msg):
	user_set = f"<@{msg.author.id}>"
	if(msg.voice_client):
		await msg.guild.voice_client.disconnect()
		await msg.reply(f"Fui desconectado do canal de voz, {user_set}.")
	else:
		await msg.reply(f"Eu não estou em nenhum canal de voz, {user_set}.")

# ================================================================
# CONFIGURE [GREET]
@bot_spright.command(name='greet')
async def on_message(ctx):
	'''
		Greeting message from the bot.
		|
		|
		`--> channel : Channel where the bot will be directed.
			`--> message.channel : Exact channel where the command was performed.
	'''

	user_set = f"<@{ctx.author.id}>"
	if user_set == "<@303321235679477760>":
		await ctx.reply(f'Hello, {user_set}! MY FATHER :heart: !!!')
	else:
		await ctx.reply(f'Hello, {user_set}!')

# ================================================================
# CONFIGURE [PRANKS]
@bot_spright.command(name="mandaTrue")
async def on_Truly(ctx):
	'''
		Spright Blue will send a fact statement
		(nothing he says should be taken seriously, the robot's purpose being just for fun)
		|
		|
		`--> list_true : List with the listed lines of the bot.
		`--> channel : Channel where the bot will be directed.
			`--> message.channel : Exact channel where the command was performed.
	'''

	list_choice = on_TrulyFunction()
	await ctx.reply(f'`{list_choice}`')

# ================================================================
# CONFIGURE [MEMES]
@bot_spright.command(name="meme")
async def on_Meme(ctx):
	'''
		Meme upload function.
		|
		|
		`--> img_set : Selected image file variable.
		`--> with open(rb) : Opens the file in binary format for reading.
		`--> channel : Channel where the bot will be directed.
			`--> message.channel : Exact channel where the command was performed.
	'''

	with open("img_memes/meme_test.png", 'rb') as img:
		img_set = discord.File(img)
		await ctx.reply(file=img_set)

# ================================================================
# CONFIGURE [WEBHOOK - EMBED(INFO)]
@bot_spright.command(name='info')
async def on_EmbedInfo(ctx):
    URL_WEBHOOK = JSON_FILE['URL_WEBHOOK']
    DESCRIPTION_EMBED = f"""
		_Bot Spright activated successfully!_{os.linesep}
		:computer: **My Creator**{os.linesep}
		_GitHub_:  https://github.com/Baku-Stark{os.linesep}\n
		:computer: **About Me**{os.linesep}
		```Players and lovers of the Yu-Gi-Oh! know me a lot (I'm a pretty annoying monster considering my level). To those who don't know... BIBIRUUU!!! I AM SPRIGHT BLUE :blue_heart: !!!``
	"""

    embed = Embed(
        url=URL_WEBHOOK,
        title="★ Spright Blue - Info",
        description=DESCRIPTION_EMBED,
        color= discord.Colour.dark_blue()
    ).set_footer(text=f"Level 2 ★ | {update_times}").set_thumbnail(url="https://media.discordapp.net/attachments/1055607254465908877/1055607254700793896/SprightBlue-Icon.png")

    await ctx.reply(embed=embed)

# ================================================================
# CONFIGURE [WEBHOOK - EMBED(HELP)]
@bot_spright.command(name="helper")
async def on_EmbedHelp(ctx):
	URL_WEBHOOK = JSON_FILE['URL_WEBHOOK']
	DESCRIPTION_EMBED = f"_Hello human! I'm here to help you!_{os.linesep}\n**The commands that are on my system are as follows:**\n"

	embed = Embed(
		url=URL_WEBHOOK,
		title="★ Spright Blue - Info",
		description=DESCRIPTION_EMBED,
		color=discord.Color.dark_blue()
	).set_footer(text=f"Level 2 ★ | {update_times}").set_thumbnail(url="https://media.discordapp.net/attachments/1055607254465908877/1055607254700793896/SprightBlue-Icon.png")

	embed.add_field(name="`/mandaTrue`", value="```A prank of my creator with his friends. Nothing written here should be taken seriously.```", inline=True)
	embed.add_field(name="`/meme`", value="```For your fun, my creator created a folder with memes to reply.```", inline=True)
	embed.add_field(name="`/helper`", value="```I'll reply a list of commands... like this one.```", inline=False)
	embed.add_field(name="`/info`", value="```Information of my existence and my creator.```", inline=True)
	embed.add_field(name="`/greet`", value="```A friendly greeting.```", inline=True)

	await ctx.reply(embed=embed)


# ================================================================
# CONFIGURE [run]
bot_spright.run(TOKEN)