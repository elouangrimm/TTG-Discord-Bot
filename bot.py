import discord
from discord.ext import commands, tasks
import os
import random
import datetime

# Made By Elouan Grimm

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# BOT VARIABLES:
username = "Tidy Tab Groups"
pfp_path = "pfp.png"
rich_presence = "Tab Organization"
extension_url = "https://chromewebstore.google.com/detail/tidy-tab-groups/fohgbkobjdckaapjimleemkolchkmebf"
ALLOWED_ROLES = ["updates", "socials", "stuff", "support", "ping", "yapper"]
tips_file = "tips.txt"
tip_time = 9
user_points = {}

# ☲☲☲☲ BOT SETUP ☲☲☲☲

def load_pfp():
    with open(pfp_path, 'rb') as f:
        return f.read()

pfp = load_pfp()

@bot.event
async def on_ready():
    activity = discord.Streaming(
        name=rich_presence,
        url=extension_url
    )
    await bot.change_presence(activity=activity)
    await bot.tree.sync()
    send_daily_tip.start()
    print(f"☲☲☲☲☲☲☲☲☲☲☲☲☲☲☲ Bot logged in as {bot.user}! Success! ☲☲☲☲☲☲☲☲☲☲☲☲☲☲☲")

def load_tips():
    with open(tips_file, "r") as file:
        tips = [line for line in file.read().splitlines() if not line.startswith("#")]
    print("Tip File Loaded")
    return tips


@tasks.loop(minutes=1)
async def send_daily_tip():
    current_time = datetime.datetime.now().time()
    if current_time.hour == tip_time and current_time.minute == 0:
        channel = bot.get_channel(1284250087995871367)
        tips = load_tips()
        tip = random.choice(tips)
        await channel.send(f"**Daily Browser Tip:** \n {tip}")
        print("Daily Tip Sent")

# ☲☲☲☲ COMMANDS ☲☲☲☲

# Add Ping Command
@bot.command()
async def addping(ctx, role: discord.Role, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if role.name not in ALLOWED_ROLES:
        await ctx.send(f"ERROR: {role.name} IS-NOT-ALLOWED-BEEPBOOP. CHOOSE-FROM: {', '.join(ALLOWED_ROLES)}. THANK YOU FOR YOUR PATIENCE. 🦾🕹️🤖🛠️")
        print("Error: Role Not Allowed")
        return

    if ctx.guild.me.guild_permissions.manage_roles:
        if role.position < ctx.guild.me.top_role.position:
            await member.add_roles(role)
            await ctx.send(f"{member.mention}! You now have the @{role.name} ping! 🎉")
            print(f"{role.name} role added!")
        else:
            await ctx.send("ERROR: CANNOT-ASSIGN-ROLE-BEEPBOOP 🤖🦾🛠️🕹️")
        print("Error: Cannot Asssign Role")
    else:
        await ctx.send("ERROR: I-CAN'T-ASSIGN-ROLES-BEEPBOOP 🕹️🛠️🦾🤖")
        print("Error: No Assigning Role Permission, add 'Manage Roles' in Discord Developer console.")

@bot.tree.command(name="addping", description="Assign a certain ping role to YOU!")
async def slash_addping(interaction: discord.Interaction, role: discord.Role, member: discord.Member = None):
    if member is None:
        member = interaction.user

    if role.name not in ALLOWED_ROLES:
        await interaction.response.send_message(f"ERROR: {role.name} IS-NOT-ALLOWED-BEEPBOOP. CHOOSE-FROM: {', '.join(ALLOWED_ROLES)}. THANK YOU FOR YOUR PATIENCE. 🦾🕹️🤖🛠️")
        print("Error: Role Not Allowed")
        return

    if interaction.guild.me.guild_permissions.manage_roles:
        if role.position < interaction.guild.me.top_role.position:
            await member.add_roles(role)
            await interaction.response.send_message(f"{member.mention}! You now have the @{role.name} ping! 🎉")
            print(f"{role.name} role added!")
        else:
            await interaction.response.send_message("ERROR: CANNOT-ASSIGN-ROLE-BEEPBOOP 🤖🦾🛠️🕹️")
            print("Error: Cannot Asssign Role")
    else:
        await interaction.response.send_message("ERROR: I-CAN'T-ASSIGN-ROLES-BEEPBOOP 🕹️🛠️🦾🤖")
        print("Error: No Assigning Role Permission, add 'Manage Roles' in Discord Developer console.")

# Tip Command

@bot.command()
async def tip(ctx):
    tips = load_tips()
    tip = random.choice(tips)
    await ctx.send(f"**Browser Tip:** {tip}")
    print("Tip Sent")

@bot.tree.command(name="tip", description="Get a random browser tip!") 
async def slash_tip(interaction: discord.Interaction):
    tips = load_tips()
    tip = random.choice(tips)
    await interaction.response.send_message(f"**Browser Tip:** {tip}")
    print("Tip Sent")

@bot.command()
async def tip_help(ctx):
    tips = load_tips()
    tip = random.choice(tips)
    await ctx.send(f"*hey! dm @elouangrimm if you have any ideas for tips to add or go to the [GitHub](<https://github.com/elouangrimm/TTG-Discord-Bot/blob/main/tips.txt>) to add some yourself! thanks!*")
    print("Tip Advert Sent")

# Help Command
@bot.command()
async def commands(ctx):
    help_text = (
        "**Here are the commands you can use:**\n"
        "`!link` - Get the link to install the Tidy Tab Groups extension.\n"
        "`!install` - Get instructions for how to install the Tidy Tab Groups extension.\n"
        "`!ping` - Check the bot's latency... and play a little game.\n"
        "`!addping <role> [member]` - Give yourself specific pings (Options: updates, socials, stuff, support, ping, yapper).\n"
        "`!commands` - Get this list! In the chat! It's Magical!\n"
        "`!offline` and `!online` - Make the bot appear Online or Offline\n"
        "`!tip` and `!tip_help` - Get a tip about your browser BEFORE THE DAILY ONE! AMAZING!\n"
    )
    await ctx.send(help_text)
    print("Help Sent")

@bot.tree.command(name="commands", description="Show available commands from this beautiful bot!")
async def slash_commands(interaction: discord.Interaction):
    help_text = (
        "**Here are the commands you can use:**\n"
        "`!link` - Get the link to install the Tidy Tab Groups extension.\n"
        "`!install` - Get instructions for how to install the Tidy Tab Groups extension.\n"
        "`!ping` - Check the bot's latency... and play a little game.\n"
        "`!addping <role> [member]` - Give yourself specific pings (Options: updates, socials, stuff, support, ping, yapper).\n"
        "`!commands` - Get this list! In the chat! It's Magical!\n"
        "`!offline` and `!online` - Make the bot appear Online or Offline\n"
        "`!tip` and `!tip_help` - Get a tip about your browser BEFORE THE DAILY ONE! AMAZING!\n"
    )
    await interaction.response.send_message(help_text)
    print("Help Sent")

# Link Command
@bot.command()
async def link(ctx):
    user = ctx.author
    await ctx.send(f"{user.mention} Here's the link to install the Tidy Tab Groups extension: https://chromewebstore.google.com/detail/tidy-tab-groups/fohgbkobjdckaapjimleemkolchkmebf")
    print("Link Sent")

@bot.tree.command(name="link", description="Get the link to install Tidy Tab Groups!")
async def slash_link(interaction: discord.Interaction):
    user = interaction.user
    await interaction.response.send_message(f"{user.mention} Here's the link to install the Tidy Tab Groups extension: https://chromewebstore.google.com/detail/tidy-tab-groups/fohgbkobjdckaapjimleemkolchkmebf")
    print("Link Sent")

# Online & Offline commands
@bot.command()
async def online(ctx):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=rich_presence))
    await ctx.send("*yawn strech* Good Morning ! 🌅👋")
    print("BOT IS ONLINE")

@bot.tree.command(name="online", description="Set the bot status to online.")
async def slash_online(interaction: discord.Interaction):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=rich_presence))
    await interaction.response.send_message("*Yawn* Good Morning ! 🌅👋")
    print("BOT IS ONLINE")

@bot.command()
async def offline(ctx):
    await bot.change_presence(status=discord.Status.offline)
    await ctx.send("Good night! *yawn* 💤")
    print("BOT IS OFFLINE")

@bot.tree.command(name="offline", description="Set the bot status to offline.")
async def slash_offline(interaction: discord.Interaction):
    await bot.change_presence(status=discord.Status.offline)
    await interaction.response.send_message("Good night! *yawn* 💤")
    print("BOT IS OFFLINE")

# Install Command
@bot.command()
async def install(ctx):
    user = ctx.author
    await ctx.send(f"{user.mention} Here’s where you can install the Tidy Tab Groups extension: [hey! click me! :P](<https://chromewebstore.google.com/detail/tidy-tab-groups/fohgbkobjdckaapjimleemkolchkmebf>) \n Then, you can click `Install` to get it and click accept. Enjoy organization! 😎😄😁")
    print("Install Instructions Sent")

@bot.tree.command(name="install", description="Get instructions for how to install the Tidy Tab Groups extension!")
async def slash_install(interaction: discord.Interaction):
    user = interaction.user
    await interaction.response.send_message(f"{user.mention} Here’s where you can install the Tidy Tab Groups extension: [hey! click me! :P](<https://chromewebstore.google.com/detail/tidy-tab-groups/fohgbkobjdckaapjimleemkolchkmebf>) \n Then, you can click `Install` to get it and click accept. Enjoy organization! 😎😄😁")
    print("Install Instructions Sent")

# Ping Command and Points Command
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    user_id = ctx.author.id
    user_points[user_id] = user_points.get(user_id, 0) + 1
    points = user_points[user_id]
    await ctx.send(f"Pong! 🏓 *(Latency: {latency} ms)*")
    print(f"Ping Received, LATENCY: {latency} ms")

@bot.tree.command(name="ping", description="Check the bot's latency and play a little game!")
async def slash_ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    user_id = interaction.user.id
    user_points[user_id] = user_points.get(user_id, 0) + 1
    points = user_points[user_id]
    await interaction.response.send_message(f"Pong! 🏓 *(Latency: {latency} ms)*")
    print(f"Ping Received, LATENCY: {latency} ms")

@bot.command()
async def ping_points(ctx, member: discord.Member = None):
    member = member or ctx.author
    user_id = member.id
    user_points[user_id] = user_points.get(user_id, 0)
    points = user_points[user_id]
    await ctx.send(f"Great Job {member.mention}! You have {points} points in Ping Pong!")
    print(f"{member.mention} has {points} points.")

@bot.tree.command(name="ping_points", description="Check how many points you or someone else has in Ping Pong!")
async def slash_ping_points(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    user_id = member.id
    user_points[user_id] = user_points.get(user_id, 0)
    points = user_points[user_id]
    await interaction.response.send_message(f"Great Job {member.mention}! You have {points} points in Ping Pong!")
    print(f"{member.mention} has {points} points.")

# Edit Command - Only through "!", not a slash command...
@bot.command()
async def edit(ctx, *, new_name: str = None):
    admin_role = discord.utils.get(ctx.guild.roles, name="admin")
    if admin_role in ctx.author.roles:
        if new_name == "reset":
            try:
                await ctx.guild.me.edit(nick=username)
                await bot.user.edit(avatar=pfp)  # Reset profile picture
                await ctx.send(f"BEEPBOOP-RESETTING-TO-ORIGINAL-SETTINGS! MY-NAME-IS-NOW **{username}**! 📸🤖")
                print(f"Bot reset to original name: {username}")
            except discord.Forbidden:
                await ctx.send("ERROR: BEEPBOOP-I-NEED-PERMISSION-TO-RESET-MY-NAME-AND-PICTURE 🔧")
        else:
            new_pfp = None
            if ctx.message.attachments:
                new_pfp = await ctx.message.attachments[0].read()
            
            try:
                if new_pfp:
                    await bot.user.edit(avatar=new_pfp)
                    await ctx.send("SUCCESS: PROFILE-PICTURE-UPDATED-BEEPBOOP 📸🤖")
                    print("Bot profile picture updated")

                if new_name:
                    await ctx.guild.me.edit(nick=new_name)
                    await ctx.send(f"BEEPBOOP-MY-NAME-IS-NOW **{new_name}**! 🦾")
                    print(f"Bot renamed to {new_name}")
                else:
                    await ctx.send("ERROR: NO-NEW-NAME-PROVIDED-BEEPBOOP 📎🛠️🤖")
            except discord.Forbidden:
                await ctx.send("ERROR: BEEPBOOP-I-NEED-PERMISSION-TO-CHANGE-MY-NAME-AND-PICTURE 🔧")
    else:
        await ctx.send("ERROR: YOU-DONT-HAVE-PERMISSIONS-TO-EDIT-ME-BEEPBOOP-ONLY-ADMINS-ALLOWED 🕹️🛠️🦾🤖")


bot.run(os.getenv("DISCORD_TOKEN"))
