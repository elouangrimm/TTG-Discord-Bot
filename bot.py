import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! 👋")

@bot.command()
async def info(ctx):
    await ctx.send("I'm a bot running on Heroku! 🎉")

@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

bot.run(os.getenv("DISCORD_TOKEN"))
