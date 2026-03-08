import discord
from discord.ext import commands
import os
import asyncio
import edge_tts

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot đã online: {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()

@bot.command()
async def say(ctx, *, text):
    voice = ctx.voice_client
    if not voice:
        await ctx.send("Bot chưa vào voice")
        return

    file = "voice.mp3"
    tts = edge_tts.Communicate(text, "vi-VN-HoaiMyNeural")
    await tts.save(file)

    voice.play(discord.FFmpegPCMAudio(file))

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

bot.run(TOKEN)
