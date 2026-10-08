import os
import discord
from discord.ext import commands

# Thiết lập Intents cần thiết cho Bot và Voice
intents = discord.Intents.default()
intents.message_content = True
intents.guild_voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("Bot voice Python đã sẵn sàng!")

@bot.command(name="join")
async def join(ctx):
    """Lệnh gọi bot vào kênh thoại của bạn"""
    if ctx.author.voice is None:
        await ctx.send("❌ Bạn cần vào một Kênh Thoại trước!")
        return
    
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"🔊 Đã vào kênh thoại: **{channel.name}**")

@bot.command(name="play")
async def play(ctx):
    """Lệnh phát file âm thanh amthanh.wav"""
    if ctx.author.voice is None:
        await ctx.send("❌ Bạn cần vào Kênh Thoại để phát nhạc!")
        return

    channel = ctx.author.voice.channel
    
    # Kết nối vào kênh voice nếu chưa vào
    if ctx.voice_client is None:
        await channel.connect()
    elif ctx.voice_client.channel != channel:
        await ctx.voice_client.move_to(channel)

    audio_file = "amthanh.wav"
    if not os.path.exists(audio_file):
        await ctx.send(f"❌ Không tìm thấy file `{audio_file}` trên thư mục chạy bot!")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    # Phát file âm thanh
    source = discord.FFmpegPCMAudio(audio_file)
    ctx.voice_client.play(source, after=lambda e: print(f"Đã phát xong audio, lỗi (nếu có): {e}"))
    
    await ctx.send("🎶 Đang bắt đầu phát âm thanh...")

@bot.command(name="leave")
async def leave(ctx):
    """Lệnh cho bot rời khỏi kênh thoại"""
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Đã rời khỏi kênh thoại.")
    else:
        await ctx.send("❌ Bot không có trong kênh thoại nào cả.")

# Lấy Token từ biến môi trường (Railway)
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("Vui lòng thiết lập biến môi trường DISCORD_TOKEN!")
else:
    bot.run(TOKEN)
