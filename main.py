# ================================================================
# IMPORTAÇÃO [pip install discord.py]
import discord
from discord.ext import commands

TOKEN = '---'
CHANNEL_ID = 'ID EM int'

intents = discord.Intents.all()
discord.Intents.members = True
discord.Intents.messages = True
discord.Intents.message_content = True
bot_spright = discord.Client(command_prefix="$", intents=intents)


@bot_spright.event
async def on_ready():
	channel = bot_spright.get_channel(CHANNEL_ID)
	letSet = f"\033[47m {bot_spright.user} \033[m"
	statusSucess = "\033[46m Conexão Establecida \033[m" #Cyan Background
	newSetSucess = f"\033[1m{statusSucess}\033[m"
	print(f"{letSet}{newSetSucess}")
	print(f"""
		BIBIRUUUUU!! I AM {bot_spright.user}

		+ Command to exit the application:
		| Press 'Ctrl + C'
		+-+---------------- x ----------------
	""")

	await channel.send('Olá, humano!!!!')


@bot_spright.event
async def on_message(message):
	if message.content.startswith('$thumb'):
		channel = bot_spright.get_channel(CHANNEL_ID)
		await channel.send('HELLO')

bot_spright.run(TOKEN)