# ================================================================
# IMPORT [os - Miscellaneous operating system interfaces]
import os

# IMPORT [wavelink n' youtube]
from youtube_dl import YoutubeDL

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
# function music [`func` = True | `silence` = False]
MUSIC_PAUSED  = False
MUSIC_PLAYING = False
# 2d array containing [song, channel]
MUSIC_QUEUE = []
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
YTDL_CONFIG = YoutubeDL(YDL_OPTIONS)
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

#searching the item on youtube
def on_searchYT(item):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try: 
            info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]

        except Exception: 
            return False

    return {'source': info['formats'][0]['url'], 'title': info['title']}
	
def play_next(ctx):
	if len(MUSIC_QUEUE) > 0:
		voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")
		MUSIC_PLAYING = True
        #get the first url
		m_url = MUSIC_QUEUE[0][0]['source']
        #remove the first element as you are currently playing it
		MUSIC_QUEUE.pop(0)
		voiceChannel.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

	else:
		MUSIC_PLAYING = False

# ================================================================
# CONFIGURE [MUSIC]
# infinite loop checking 
async def play_music(ctx, urlYT):
	server = ctx.message.guild
	voiceChannel = server.voice_client

	if voiceChannel != None:
		MUSIC_PLAYING = True

		data_music = YTDL_CONFIG.extract_info(url=urlYT, download=False)
		m_url = data_music['url']

		voiceChannel.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS, executable='ffmpeg/bin/ffmpeg.exe'), after=lambda e: play_next(ctx))

	else:
		MUSIC_PLAYING = False

@bot_spright.command(name="play")
async def on_Music(ctx, urlYT:str):
	query = " ".join(urlYT)
	user_set = f"<@{ctx.author.id}>"
	data_music = YTDL_CONFIG.extract_info(url=urlYT, download=False)

	if not ctx.message.author.voice:
		await ctx.reply(f"❌ **Enter some voice channel,** {user_set}**...**")
		return

	else:
		voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")
		await voiceChannel.connect()

		await ctx.reply(f"🎧 **{data_music['title']}\n\n🖥️ {data_music['channel']}**")

		song = on_searchYT(query)

		if type(song) == type(True):
			await ctx.reply("❌ **Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.**")

		elif MUSIC_PAUSED:
			voiceChannel.resume(ctx)
			
		else:
			await ctx.send("✔️ **Song added to the queue**")
			MUSIC_QUEUE.append([song, voiceChannel])
                
			if MUSIC_PLAYING == False:
				await play_music(ctx, urlYT)

@bot_spright.command(name="pause")
async def pause(ctx, *args):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")
	if MUSIC_PLAYING:
		MUSIC_PLAYING = False
		MUSIC_PAUSED = True
		voiceChannel.pause()

	elif MUSIC_PAUSED:
		MUSIC_PAUSED = False
		MUSIC_PLAYING = True
		voiceChannel.resume()

@bot_spright.command(name = "resume")
async def resume(ctx, *args):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")

	if MUSIC_PAUSED:
		MUSIC_PAUSED = False
		MUSIC_PLAYING = True
		voiceChannel.resume()

@bot_spright.command(name="skip")
async def skip(ctx):
	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")

	if voiceChannel != None:
		voiceChannel.stop()
        #try to play next in the queue if it exists
		await play_music(ctx)

@bot_spright.command(name="queue")
async def queue(ctx):
    retval = ""
    for i in range(0, len(MUSIC_QUEUE)):
        # display a max of 5 songs in the current queue
        if (i > 4): break
        retval += MUSIC_QUEUE[i][0]['title'] + "\n"

    if retval != "":
        await ctx.reply(retval)
    else:
        await ctx.reply("❌ **No music in queue**")

@bot_spright.command(name="clear")
async def clear(ctx):
	server = ctx.message.guild
	voiceChannel = server.voice_client

	if voiceChannel != None and MUSIC_PLAYING:
		voiceChannel.stop()
		MUSIC_QUEUE = []
		await ctx.reply("✔️ **Music queue cleared**")

	else:
		await ctx.reply("❌ **There is no queue to clear.**")

@bot_spright.command(name="leave")
async def offChannel(ctx):
	user_set = f"<@{ctx.author.id}>"
	
	if (ctx.voice_client):
		await ctx.guild.voice_client.disconnect()
		await ctx.reply(f"✔️ **I was disconnected from the voice channel successfully,** {user_set}.")

	else:
		await ctx.reply(f"❌ **I'm not on any voice channels,** {user_set}.")

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
	print(connection_test())

	# Panel Greeting
	print(Panel.fit(f"[bold blue]Hi, human!!!\nI am {bot_spright.user}", border_style="cyan", title="Bot Discord"))

	# Tree bot_spright
	tree = Tree("[bold white]Command to exit the application")
	tree.add("command : Press [cyan]'Ctrl + C'[/cyan]")
	print(tree)

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
# CONFIGURE [WEBHOOK - EMBED(INFO)]
@bot_spright.command(name='info')
async def on_EmbedInfo(ctx):
    URL_WEBHOOK = JSON_FILE['URL_WEBHOOK']
    DESCRIPTION_EMBED = """
		_Bot Spright activated successfully!_
		💻 **My Creator**\n
		GitHub:  https://github.com/Baku-Stark\n\n
		💻 **About Me**\n
		```Players and lovers of the Yu-Gi-Oh! know me a lot (I'm a pretty annoying monster considering my level). To those who don't know... BIBIRUUU!!! I AM SPRIGHT BLUE 💙 !!!```
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
	DESCRIPTION_EMBED = f"_Hello human! I'm here to help you!_{os.linesep}\n**The bot_spright that are on my system are as follows:**\n"

	embed = Embed(
		url=URL_WEBHOOK,
		title="★ Spright Blue - Info",
		description=DESCRIPTION_EMBED,
		color=discord.Color.dark_blue()
	).set_footer(text=f"Level 2 ★ | {update_times}").set_thumbnail(url="https://media.discordapp.net/attachments/1055607254465908877/1055607254700793896/SprightBlue-Icon.png")

	# title[😂 Funny]
	embed.add_field(name="▬▬▬▬▬▬", value="😂 **Funny**", inline=False)
	# content
	embed.add_field(name="`/mandaTrue`", value="```A prank of my creator with his friends. Nothing written here should be taken seriously.```", inline=True)
	embed.add_field(name="`/meme`", value="```For your fun, my creator created a folder with memes to reply.```", inline=True)
	embed.add_field(name="`/greet`", value="```A friendly greeting.```", inline=True)

	# title[🕹️ Control]
	embed.add_field(name="▬▬▬▬▬▬", value="🕹️ **Control**", inline=False)
	# content
	embed.add_field(name="`/helper`", value="```I'll reply a list of bot_spright... like this one.```", inline=True)
	embed.add_field(name="`/info`", value="```Information of my existence and my creator.```", inline=True)

	# title[🎧 Music]
	embed.add_field(name="▬▬▬▬▬▬", value="🎧 **Music**", inline=False)
	# title[🎧 Music]
	embed.add_field(name="`/play <url_YouTube>`", value="```I'm going to join the voice channel to play a song.```", inline=True)
	embed.add_field(name="`/leave`", value="```You will take me off the voice call by interrupting your music.```", inline=True)

	await ctx.reply(embed=embed)

# ================================================================
# CONFIGURE [run]
bot_spright.run(TOKEN)