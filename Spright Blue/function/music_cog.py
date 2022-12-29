from ast import alias
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        bot = bot
    
        #all the music related stuff
        is_playing = False
        is_paused = False

        # 2d array containing [song, channel]
        music_queue = []
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        var_vc = None

    #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(music_queue) > 0:
            is_playing = True

            #get the first url
            m_url = music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            music_queue.pop(0)

            var_vc.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS), after=lambda e: play_next())
        else:
            is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):
        if len(music_queue) > 0:
            is_playing = True

            m_url = music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected
            if var_vc == None or not var_vc.is_connected():
                var_vc = await music_queue[0][1].connect()

                #in case we fail to connect
                if var_vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await var_vc.move_to(music_queue[0][1])
            
            #remove the first element as you are currently playing it
            music_queue.pop(0)

            var_vc.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS), after=lambda e: play_next())
        else:
            is_playing = False

    @commands.command(name="play")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif is_paused:
            var_vc.resume()
        else:
            song = search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                music_queue.append([song, voice_channel])
                
                if is_playing == False:
                    await play_music(ctx)

    @commands.command(name="pause")
    async def pause(self, ctx, *args):
        if is_playing:
            is_playing = False
            is_paused = True
            var_vc.pause()

        elif is_paused:
            is_paused = False
            is_playing = True
            var_vc.resume()

    @commands.command(name = "resume")
    async def resume(self, ctx, *args):
        if is_paused:
            is_paused = False
            is_playing = True
            var_vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if var_vc != None and var_vc:
            var_vc.stop()
            #try to play next in the queue if it exists
            await play_music(ctx)


    @commands.command(name="queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="clear")
    async def clear(self, ctx):
        if var_vc != None and is_playing:
            var_vc.stop()
        music_queue = []
        await ctx.send("Music queue cleared")

    @commands.command(name="leave")
    async def offChannel(self, ctx):
        is_playing = False
        is_paused = False
        await var_vc.disconnect()