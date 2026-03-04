import discord
from discord.ext import commands
import os
import asyncio

from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} запущений і готовий!")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash-команди синхронізовані: {len(synced)}")
    except Exception as e:
        print(e)

async def load_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())
