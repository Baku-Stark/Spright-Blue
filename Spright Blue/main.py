# ================================================================
# IMPORT [console]
import console
from console.utils import set_title

# IMPORT [rich - dashboard(console)]
from rich.console import group
from rich.panel import Panel

# IMPORT [os - Miscellaneous operating system interfaces]
import os

# IMPORT [PIL > Image]
from PIL import Image

# IMPORT [requests - images]
import requests

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

# IMPORT [datetime - calendar]
from datetime import datetime
update_times = datetime.strftime(datetime.now(),'20%y/%m/%d [%I:%M]')

# IMPORT [rich - dashboard(console)]
from rich import print
from rich.tree import Tree
from rich.panel import Panel

# IMPORT [cogs[folder] > files]
from cogs.embed import *
from cogs.music import *

# IMPORT [function[folder] > files]
from function.mandaTrue import on_TrulyFunction
from function.connection import connection_test
from function.meme import memeSelect
from function.hist import historyWrite

# ================================================================
# IMPORT [pip install discord.py]
import discord
from discord import Embed
from discord.ext import commands
# CONFIGURE [Discord]
intents = discord.Intents.all()
discord.Intents.members = True
discord.Intents.messages = True
discord.Intents.message_content = True
# variavél [from discord.ext import bot_spright]
bot_spright = commands.Bot(command_prefix="/", intents=intents)
CHANNEL_ID = JSON_FILE['CHANNEL_ID']
channel = bot_spright.get_channel(CHANNEL_ID)
TOKEN = JSON_FILE['TOKEN']

# ================================================================
# APPLICATION [Main Function ACTIVE]
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
	os.system('cls')
	set_title('Discord Bot - Spright Blue')
	print(connection_test())

	# Panel Greeting
	print(Panel(f"[bold blue]Hi, human!!!\nI am {bot_spright.user}", border_style="cyan", title="Bot Discord"))

	# [COGS]
	try:
		# [EMBED]
		print(Panel(cog_EmbedStatus()))
		await bot_spright.add_cog(EmbedClass(bot_spright))

		# [MUSIC]
		print(Panel(cog_MusicStatus()))
		await bot_spright.add_cog(MusicClass(bot_spright))

	except ModuleNotFoundError:
		@group()
		def error_Module():
			status = yield Panel("[bold]COGS > embed.py ACTIVED![/bold]", style="red")
			return status
		
		print(Panel(error_Module()))

	# Tree bot_spright
	tree = Tree("[bold white]Command to exit the application")
	tree.add("command : Press [cyan]'Ctrl + C'[/cyan]")
	print(tree)

# ================================================================
# CONFIGURE [TESTE]
@bot_spright.command(name='pisei')
async def function(ctx, user_set:discord.User):
	'''
		`Pisei Na Merda` meme generator.
		|
		|
		`--> ctx : Context
		`--> user_set : Mentioned user.
			`--> userID : Mentioned user ID.
			`--> userAvatar : Mentioned user AVATAR.
	'''
	userID = user_set.id
	userAvatar = user_set.avatar

	if userID == 303321235679477760:
		await ctx.reply("😡 You cannot tag my creator in this meme.")
		userID = ctx.author.id
		userAvatar = ctx.author.avatar
		# save icon[user_set]
		image_url = str(userAvatar)
		myfile = requests.get(image_url)
		open(f"img_memes/users/{str(userID)}.png", 'wb').write(myfile.content)

		# pisei_na_merda.jpg [275x400]
		base_image = Image.open('img_memes/templates/pisei_na_merda.jpg')
		icon_user = Image.open(f'img_memes/users/{userID}.png').convert('RGBA')

		position = base_image.size
		# icone do usuario para novo tamanho [100x110]
		newSize = (97, 110)
		icon_user = icon_user.resize(newSize)
		# posição do ícone
		new_pos = 75, 250
		transparent = Image.new(mode='RGBA', size=position, color=(0, 0, 0, 0))
		transparent.paste(base_image, (0, 0))
		transparent.paste(icon_user, new_pos, icon_user)
		image_mode = base_image.mode
		if image_mode == 'RGB':
				transparent = transparent.convert(image_mode)

		else:
			transparent = transparent.convert('P')
		transparent.save('img_memes/img_create/teste.jpg', optimize=True, quality=100)

		with open(f'img_memes/img_create/meme_{userID}.jpg', 'rb') as img:
			img_set = discord.File(img)
			await ctx.reply(file=img_set)

	else:
		image_url = str(userAvatar)
		myfile = requests.get(image_url)
		open(f"img_memes/users/{str(userID)}.png", 'wb').write(myfile.content)

		# pisei_na_merda.jpg [275x400]
		base_image = Image.open('img_memes/templates/pisei_na_merda.jpg')
		icon_user = Image.open(f'img_memes/users/{userID}.png').convert('RGBA')

		position = base_image.size
		# icone do usuario para novo tamanho [100x110]
		newSize = (97, 110)
		icon_user = icon_user.resize(newSize)
		# posição do ícone
		new_pos = 75, 250
		transparent = Image.new(mode='RGBA', size=position, color=(0, 0, 0, 0))
		transparent.paste(base_image, (0, 0))
		transparent.paste(icon_user, new_pos, icon_user)
		image_mode = base_image.mode
		if image_mode == 'RGB':
				transparent = transparent.convert(image_mode)

		else:
			transparent = transparent.convert('P')
		transparent.save(f'img_memes/img_create/meme_{userID}.jpg', optimize=True, quality=100)

		with open(f'img_memes/img_create/meme_{userID}.jpg', 'rb') as img:
			img_set = discord.File(img)
			await ctx.reply(file=img_set)

# ================================================================
# CONFIGURE [GREET]
@bot_spright.command(name='greet')
async def on_message(ctx):
	'''
		Greeting message from the bot.
		|
		|
		`--> ctx.author : Message author name (example#1234).
			`--> ctx.author.id : Message author ID to mention.
			`--> ctx.guild.icon.url : Icon's server.
			`--> ctx.guild.owner : Server owner.		
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
async def on_Meme(ctx, server_select: str):
	'''
		Meme upload function.
		|
		|
		`--> server_select : Server selected[tcgserver/here].
		`--> ctx.guild.id : Message's current server ID.
		`--> image_choice : Randomly selected image from the list[memeSelect].
			`--> img_set : Selected image file variable.
		`--> with open(rb) : Opens the file in binary format for reading.
		`--> channel : Channel where the bot will be directed.
	'''
	if str(ctx.guild.id) == "758412990163714139" and server_select.lower() == "tcgserver":
		image_choice = memeSelect("servertcg")

		await ctx.send(f"✔️ This is the '{ctx.guild.name}' server. That's why it has a special meme folder. See one of the memes:")

		with open(f"img_memes/servertcg/{image_choice}", 'rb') as img:
			img_set = discord.File(img)
			
			await ctx.reply(file=img_set)

	elif str(ctx.guild.id) != "758412990163714139" and server_select.lower() == "tcgserver":
		await ctx.reply("❌ This is not `Only 🇧🇷 TAG` server.")
		

	elif server_select.lower() == "here":
		image_choice = memeSelect("other_server")

		with open(f"img_memes/o_servers/{image_choice}", 'rb') as img:
			img_set = discord.File(img)
			await ctx.reply(file=img_set)

	else:
		await ctx.reply("❌ Something went wrong...")

@bot_spright.command(name="save")
async def on_MemeSave(ctx, folder: str):
	image_url = str(ctx.message.attachments[0].url)
	ftype = image_url.split('/')[-1]
	myfile = requests.get(image_url)
	
	if folder.lower() == "servertcg" or folder.lower() == "o_servers":
		open(f"img_memes/{folder}/{ftype}", 'wb').write(myfile.content)

		#  history [function]
		historyWrite(ctx.author, image_url, folder, update_times, ctx.guild.name, ctx.guild.id)
		
		user_set = f"<@{ctx.author.id}>"
		await ctx.reply(f"✔️ The image was successfully saved, {user_set}!")
		
	else:
		URL_WEBHOOK = JSON_FILE['URL_WEBHOOK']
		embed = Embed(
			url=URL_WEBHOOK,
			title="★ Spright Blue - Info",
			description="❌ Directory not found. Use `serverTCG` or `o_servers`.",
			color= discord.Colour.dark_blue()
    	).set_footer(text=f"Level 2 ★ | {update_times}")
		
		await ctx.reply(embed=embed)

# ================================================================
# CONFIGURE [run]
bot_spright.run(TOKEN)