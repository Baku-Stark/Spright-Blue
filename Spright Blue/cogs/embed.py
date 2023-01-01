# ================================================================
# IMPORT [rich - dashboard(console)]
from rich.console import group
from rich.panel import Panel

# IMPORT [pip install discord.py]
import discord
from discord import Embed
from discord.ext import commands

# IMPORT [datetime - calendar]
from datetime import datetime
update_times = datetime.strftime(datetime.now(),'20%y/%m/%d [%I:%M]')

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

class EmbedClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ================================================================
    # CONFIGURE [WEBHOOK - EMBED(INFO)]
    @commands.command(name='info')
    async def on_EmbedInfo(self, ctx):
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
    @commands.command(name="helper")
    async def on_EmbedHelp(self, ctx):
        URL_WEBHOOK = JSON_FILE['URL_WEBHOOK']
        DESCRIPTION_EMBED = "_Hello human! I'm here to help you!_\n\n**The commands that are on my system are as follows:**\n"

        embed = Embed(
            url=URL_WEBHOOK,
            title="★ Spright Blue - Info",
            description=DESCRIPTION_EMBED,
            color=discord.Color.dark_blue()
        ).set_footer(text=f"Level 2 ★ | {update_times}").set_thumbnail(url="https://media.discordapp.net/attachments/1055607254465908877/1055607254700793896/SprightBlue-Icon.png")

        # title[😂 Funny]
        embed.add_field(name="▬▬▬ 😂 ▬▬▬", value="**Funny**", inline=False)
        # content
        embed.add_field(name="`/mandaTrue`", value="```A prank of my creator with his friends. Nothing written here should be taken seriously.```", inline=True)
        embed.add_field(name="`/meme`", value="```For your fun, my creator created a folder with memes to reply.```", inline=True)
        embed.add_field(name="`/greet`", value="```A friendly greeting.```", inline=True)

        # title[🕹️ Control]
        embed.add_field(name="▬▬▬ 🕹️ ▬▬▬", value="**Control**", inline=False)
        # content
        embed.add_field(name="`/helper`", value="```I'll reply a list of commands... like this one.```", inline=True)
        embed.add_field(name="`/info`", value="```Information of my existence and my creator.```", inline=True)

        # title[🎧 Music]
        embed.add_field(name="▬▬▬ 🎧 ▬▬▬", value="**Music**", inline=False)
        # title[🎧 Music]
        embed.add_field(name="`/play <url_YouTube>`", value="```I'm going to join the voice channel to play a song.```", inline=True)
        embed.add_field(name="`/leave`", value="```You will take me off the voice call by interrupting your music.```", inline=True)

        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(EmbedClass(client))

@group()
def cogEmbedStatus():
    status = yield Panel("[bold]COGS > embed.py ACTIVED![/bold]", style="blue")
    return status
