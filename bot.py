import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True  # Ensure the bot can read messages
bot = commands.Bot(command_prefix="!", intents=intents)

# BOT VARIABLES:
rich_presence = "Tab Organization"
ALLOWED_ROLES = ["updates", "socials", "stuff", "support", "ping", "yapper"]
user_message_counts = {}  # Dictionary to keep track of user message counts

# ☲☲☲☲ BOT SETUP ☲☲☲☲

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=rich_presence))
    await bot.tree.sync()
    print(f"We have logged in as {bot.user}")

# Count messages sent by users
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id not in user_message_counts:
        user_message_counts[message.author.id] = 0
    user_message_counts[message.author.id] += 1
    await bot.process_commands(message)

# ☲☲☲☲ COMMANDS ☲☲☲☲

# Add Ping Command
@bot.command()
async def addping(ctx, role: discord.Role, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if role.name not in ALLOWED_ROLES:
        await ctx.send(f"ERROR: {role.name} IS-NOT-ALLOWED-BEEPBOOP. CHOOSE-FROM: {', '.join(ALLOWED_ROLES)}. THANK YOU FOR YOUR PATIENCE. 🦾🕹️🤖🛠️")
        return

    if ctx.guild.me.guild_permissions.manage_roles:
        if role.position < ctx.guild.me.top_role.position:
            await member.add_roles(role)
            await ctx.send(f"{member.mention}! You now have the @{role.name} ping! 🎉")
        else:
            await ctx.send("ERROR: CANNOT-ASSIGN-ROLE-BEEPBOOP 🤖🦾🛠️🕹️")
    else:
        await ctx.send("ERROR: I-CAN'T-ASSIGN-ROLES-BEEPBOOP 🕹️🛠️🦾🤖")

@bot.tree.command(name="addping", description="Assign a certain ping role to a user")
async def slash_addping(interaction: discord.Interaction, role: discord.Role, member: discord.Member = None):
    if member is None:
        member = interaction.user

    if role.name not in ALLOWED_ROLES:
        await interaction.response.send_message(f"ERROR: {role.name} IS-NOT-ALLOWED-BEEPBOOP. CHOOSE-FROM: {', '.join(ALLOWED_ROLES)}. THANK YOU FOR YOUR PATIENCE. 🦾🕹️🤖🛠️")
        return

    if interaction.guild.me.guild_permissions.manage_roles:
        if role.position < interaction.guild.me.top_role.position:
            await member.add_roles(role)
            await interaction.response.send_message(f"{member.mention}! You now have the @{role.name} ping! 🎉")
        else:
            await interaction.response.send_message("ERROR: CANNOT-ASSIGN-ROLE-BEEPBOOP 🤖🦾🛠️🕹️")
    else:
        await interaction.response.send_message("ERROR: I-CAN'T-ASSIGN-ROLES-BEEPBOOP 🕹️🛠️🦾🤖")

# Help Command
@bot.command()
async def bot_help(ctx):
    help_text = (
        "Here are the commands you can use:\n"
        "`!link` - Get the link to install the Tidy Tab Groups extension.\n"
        "`!install` - Get instructions for how to install the Tidy Tab Groups extension.\n"
        "`!ping` - Check the bot's latency.\n"
        "`!addping <role> [member]` - Give yourself specific pings (Options: updates, socials, stuff, support, ping, yapper).\n"
        "`!stats` - Show the number of messages you've sent."
    )
    await ctx.send(help_text)

@bot.tree.command(name="bot-help", description="Show available commands")
async def slash_bot_help(interaction: discord.Interaction):
    help_text = (
        "Here are the commands you can use:\n"
        "`!link` - Get the link to install the Tidy Tab Groups extension.\n"
        "`!install` - Get instructions for how to install the Tidy Tab Groups extension.\n"
        "`!ping` - Check the bot's latency.\n"
        "`!addping <role> [member]` - Give yourself specific pings (Options: updates, socials, stuff, support, ping, yapper).\n"
        "`!stats` - Show the number of messages you've sent."
    )
    await interaction.response.send_message(help_text)

# User Stats Command
@bot.command()
async def stats(ctx):
    count = user_message_counts.get(ctx.author.id, 0)
    await ctx.send(f"{ctx.author.mention}, you have sent **{count}** messages in this server! Great Job!📊")

@bot.tree.command(name="stats", description="Show your message count")
async def slash_stats(interaction: discord.Interaction):
    count = user_message_counts.get(interaction.user.id, 0)
    await interaction.response.send_message(f"{interaction.user.mention}, you have sent **{count}** messages in this server! Great Job!📊")

# Link Command
@bot.command()
async def link(ctx):
    user = ctx.author
    await ctx.send(f"{user.mention} Here's the link to install the Tidy Tab Groups extension: https://chromewebstore.google.com/detail/tidy-tab-groups/fohgbkobjdckaapjimleemkolchkmebf")

@bot.tree.command(name="link", description="Get the link to install Tidy Tab Groups")
async def slash_link(interaction: discord.Interaction):
    user = interaction.user
    await interaction.response.send_message(f"{user.mention} Here's the link to install the Tidy Tab Groups extension: https://chromewebstore.google.com/detail/tidy-tab-groups/fohgbkobjdckaapjimleemkolchkmebf")

# Install Command
@bot.command()
async def install(ctx):
    user = ctx.author
    await ctx.send(f"{user.mention} Here’s where you can install the Tidy Tab Groups extension: [hey! click me! :P](<https://chromewebstore.google.com/detail/tidy-tab-groups/fohgbkobjdckaapjimleemkolchkmebf>) \n Then, you can click `Install` to get it and click accept. Enjoy organization! 😎😄😁")

@bot.tree.command(name="install", description="Get instructions for how to install the Tidy Tab Groups extension")
async def slash_install(interaction: discord.Interaction):
    user = interaction.user
    await interaction.response.send_message(f"{user.mention} Here’s where you can install the Tidy Tab Groups extension: [hey! click me! :P](<https://chromewebstore.google.com/detail/tidy-tab-groups/fohgbkobjdckaapjimleemkolchkmebf>) \n Then, you can click `Install` to get it and click accept. Enjoy organization! 😎😄😁")

# Ping Command
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! 🏓 *(Latency: {latency} ms)*")

@bot.tree.command(name="ping", description="Check the bot's latency")
async def slash_ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! 🏓 *(Latency: {latency} ms)*")

# ☲☲☲☲ BOT SETUP & SYNC ☲☲☲☲

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"We have logged in as {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))