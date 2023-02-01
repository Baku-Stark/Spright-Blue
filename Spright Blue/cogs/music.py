# ================================================================
# IMPORT [wavelink n' youtube]
from youtube_dl import YoutubeDL

# IMPORT [os - Miscellaneous operating system interfaces]
import os

# IMPORT [rich - dashboard(console)]
from rich.console import group
from rich.panel import Panel

# IMPORT [pip install discord.py]
import discord
from discord import Embed
from discord.ext import commands

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

class MusicClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ================================================================
        # function music
        self.MUSIC_PAUSED  = False
        self.MUSIC_PLAYING = False
        # 2d array containing [song, channel]
        self.MUSIC_QUEUE = []
        self.YDL_OPTIONS = {
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
        self.YTDL_CONFIG = YoutubeDL(self.YDL_OPTIONS)
        self.FFMPEG_DIR = "ffmpeg/bin/ffmpeg.exe"
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    #searching the item on youtube
    def on_searchYT(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]

            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}
        
    def play_next(self, ctx):
        if len(self.MUSIC_QUEUE) > 0:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")
            self.MUSIC_PLAYING = True
            #get the first url
            m_url = self.MUSIC_QUEUE[0][0]['source']
            #remove the first element as you are currently playing it
            self.MUSIC_QUEUE.pop(0)
            voiceChannel.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))

        else:
            self.MUSIC_PLAYING = False

    # ================================================================
    # CONFIGURE [MUSIC]
    # infinite loop checking 
    async def play_music(self, ctx, urlYT):
        server = ctx.message.guild
        voiceChannel = server.voice_client

        if voiceChannel != None:
            self.MUSIC_PLAYING = True

            data_music = self.YTDL_CONFIG.extract_info(url=urlYT, download=False)
            m_url = data_music['url']

            voiceChannel.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS, executable=self.FFMPEG_DIR), after=lambda e: self.play_next(ctx))

        else:
            self.MUSIC_PLAYING = False

    @commands.command(name="play")
    async def on_Music(self, ctx, urlYT:str):
        query = " ".join(urlYT)
        user_set = f"<@{ctx.author.id}>"
        data_music = self.YTDL_CONFIG.extract_info(url=urlYT, download=False)

        if not ctx.message.author.voice:
            await ctx.reply(f"❌ **Enter some voice channel,** {user_set}**...**")
            return

        else:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")
            await voiceChannel.connect()

            await ctx.reply(f"🎧 **{data_music['title']}\n\n🖥️ {data_music['channel']}**")

            song = self.on_searchYT(query)

            if type(song) == type(True):
                await ctx.reply("❌ **Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.**")

            elif self.MUSIC_PAUSED:
                voiceChannel.resume(ctx)
                
            else:
                await ctx.send("✔️ **Song added to the queue**")
                self.MUSIC_QUEUE.append([song, voiceChannel])
                    
                if self.MUSIC_PLAYING == False:
                    await self.play_music(ctx, urlYT)

    @commands.command(name="pause")
    async def pause(self, ctx, *args):
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")
        if self.MUSIC_PLAYING:
            self.MUSIC_PLAYING = False
            self.MUSIC_PAUSED = True
            voiceChannel.pause()

        elif self.MUSIC_PAUSED:
            self.MUSIC_PAUSED = False
            self.MUSIC_PLAYING = True
            voiceChannel.resume()

    @commands.command(name = "resume")
    async def resume(self, ctx, *args):
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")

        if self.MUSIC_PAUSED:
            self.MUSIC_PAUSED = False
            self.MUSIC_PLAYING = True
            voiceChannel.resume()

    @commands.command(name="skip")
    async def skip(self, ctx):
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=f"{ctx.message.author.voice.channel}")

        if voiceChannel != None:
            voiceChannel.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)

    @commands.command(name="queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.MUSIC_QUEUE)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.MUSIC_QUEUE[i][0]['title'] + "\n"

        if retval != "":
            await ctx.reply(retval)
        else:
            await ctx.reply("❌ **No music in queue**")

    @commands.command(name="clear")
    async def clear(self, ctx):
        server = ctx.message.guild
        voiceChannel = server.voice_client

        if voiceChannel != None and self.MUSIC_PLAYING:
            voiceChannel.stop()
            self.MUSIC_QUEUE = []
            await ctx.reply("✔️ **Music queue cleared**")

        else:
            await ctx.reply("❌ **There is no queue to clear.**")

    @commands.command(name="leave")
    async def offChannel(self, ctx):
        user_set = f"<@{ctx.author.id}>"
        
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.reply(f"✔️ **I was disconnected from the voice channel successfully,** {user_set}.")

        else:
            await ctx.reply(f"❌ **I'm not on any voice channels,** {user_set}.")


#  -----------
async def setup(client):
    await client.add_cog(MusicClass(client))

@group()
def cog_MusicStatus():
    status = yield Panel("[bold]COGS > music.py ACTIVED![/bold]", style="blue")
    return status