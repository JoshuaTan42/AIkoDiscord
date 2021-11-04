import discord
from discord.ext import commands
import yt_dlp
import os
import logging
import asyncio
from Functions.commands import *
from AI.DialoGPT import conversation
from datetime import datetime

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='~')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'}],
    'outtmpl': 'music.mp3'}

music_queue = []
music_name = {}


def report(guild):
    online = 0
    idle = 0
    offline = 0

    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        elif str(m.status) == "offline":
            offline += 1
        else:
            idle += 1

    return online, idle, offline


async def background_task():
    await client.wait_until_ready()
    global server
    server = client.get_guild("<Server_ID>")
    while not client.is_closed():
        try:
            if len(music_queue) > 0 and vc and not vc.is_playing():
                if os.path.exists("music.mp3"):
                    os.remove("music.mp3")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    music_name.pop(music_queue[0])
                    ydl.download([music_queue.pop(0)])
                vc.play(discord.FFmpegPCMAudio('music.mp3'), after=lambda x: os.remove("music.mp3"))
            await asyncio.sleep(1)
        except Exception as e:
            logging.exception(exc_info=True)
            await asyncio.sleep(0.2)


@client.event
async def on_ready():
    global server
    global chat_history_ids
    global chat_round
    global server_ready
    print(f"Login Successful: {client.user}")
    chat_history_ids = None
    chat_round = 0


@client.event
async def on_message(message):
    global server
    global vc
    global chat_history_ids
    global chat_round
    global music_name
    global music_queue

    if "~" in message.content:
        print(f"{datetime.now()}: {message.channel}: {message.author}: {message.content}")
        if "~help" in message.content.lower():
            await message.channel.send(help_cmd())

        if "~server report" in message.content.lower():
            online, idle, offline = report(server)
            await message.channel.send(server_report_cmd(online, idle, offline, server))

        if "~join" in message.content:
            music_queue = []
            music_name = {}
            try:
                channel = message.author.voice.channel
                vc = await channel.connect()
                print(f"===Connected to {channel}===")
            except Exception as e:
                await message.channel.send(HandleExceptions.ClientError.vc_error(e))

        if message.content.startswith("~tts"):
            vc = server.voice_client
            try:
                text = message.content.lower().split(' ')
                TextToSpeech(text).save("tts.mp3")
                if not vc.is_playing():
                    vc.play(discord.FFmpegPCMAudio('tts.mp3'), after=None)
            except Exception as e:
                await message.channel.send(HandleExceptions.ServerError.default_unknown_error(e))
                logging.exception(exc_info=True)

        if message.content.startswith("~p") or message.content.startswith("~play"):
            vc = server.voice_client
            try:
                content = message.content.split(' ')
                Music(music_queue, music_name, ydl_opts).play(content)

            except Exception as e:
                await message.channel.send(HandleExceptions.ServerError.default_unknown_error(e))
                logging.exception(exc_info=True)

        if message.content.startswith("~q") or message.content.startswith("~queue"):
            await message.channel.send(Music(music_queue, music_name, ydl_opts).queue())

        if message.content.startswith("~c") or message.content.startswith("~clear"):
            music_queue = []
            music_name = {}
            await message.channel.send("Queue has been cleared")

        if message.content.startswith("~stop"):
            if vc.is_playing():
                vc.stop()
                await message.channel.send("Stopped the current song")

        if "~leave" in message.content.lower():
            music_queue = []
            music_name = {}
            channel = message.author.voice.channel
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await message.channel.send("Bye Bye :wave: ")
                    await vc.disconnect()
                    print(f"===Disconnected from {channel}===")

    if message.content.startswith(">"):
        vc = server.voice_client
        text = message.content.lower().split('>')
        text = ' '.join(text)
        print(f"Input: {text}")
        reply = conversation(text)
        print(f"Reply: {reply}")
        await message.channel.send(reply)



client.loop.create_task(background_task())
client.run("<Insert_Token>")
bot.run("<Insert_Token>")