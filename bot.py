import discord
from discord.ext import commands
import os
import edge_tts
import yt_dlp
import random

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🚀 Bot online: {bot.user}")

# ----------------
# PING
# ----------------
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# ----------------
# JOIN VOICE
# ----------------
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("✅ Bot đã vào voice")

# ----------------
# LEAVE VOICE
# ----------------
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Bot đã rời voice")

# ----------------
# BOT NÓI TIẾNG VIỆT
# ----------------
@bot.command()
async def say(ctx, *, text):
    voice = ctx.voice_client

    if not voice:
        await ctx.send("❌ Bot chưa vào voice")
        return

    file = "voice.mp3"

    tts = edge_tts.Communicate(text, "vi-VN-HoaiMyNeural")
    await tts.save(file)

    voice.play(discord.FFmpegPCMAudio(file))

# ----------------
# PHÁT NHẠC YOUTUBE
# ----------------
@bot.command()
async def play(ctx, url):

    vc = ctx.voice_client

    if not vc:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            vc = await channel.connect()
        else:
            await ctx.send("❌ Bạn chưa vào voice")
            return

    ydl_opts = {"format": "bestaudio"}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info["url"]

    vc.play(discord.FFmpegPCMAudio(url2))

    await ctx.send("🎵 Đang phát nhạc")

# ----------------
# MINI GAME
# ----------------
@bot.command()
async def guess(ctx):

    number = random.randint(1, 10)

    await ctx.send("🎮 Đoán số từ 1 - 10")

    def check(m):
        return m.author == ctx.author

    msg = await bot.wait_for("message", check=check)

    if int(msg.content) == number:
        await ctx.send("🎉 Đúng rồi!")
    else:
        await ctx.send(f"❌ Sai! số là {number}")

bot.run(TOKEN)
