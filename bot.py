import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True  # مهم عشان نقدر نجيب الأعضاء
bot = commands.Bot(command_prefix="!", intents=intents)
log_channel = None

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} | Slash commands synced")

@bot.tree.command(name="embed", description="Embed builder")
@app_commands.describe(title="Title", des="Description", footer="Footer", author="Author", color="Hex color (ex: FF0000)")
async def embed(interaction: discord.Interaction, title: str, des: str, footer: str, author: str, color: str):
    try:
        hex_color = int(color, 16)
        c = discord.Color(hex_color)
    except:
        await interaction.response.send_message("Invalid color code. Use hex like FF0000.", ephemeral=True)
        return

    embed = discord.Embed(title=title, description=des, color=c)
    embed.set_author(name=author, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
    embed.set_footer(text=footer)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kick", description="Kick a user or bot from the server")
@app_commands.describe(member="Select a member (can be a bot)", reason="Reason for kicking")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("❌ You don't have permission to kick members.", ephemeral=True)
        return
    elif log_channel == None:
    	await interaction.response.send_message("Please set Your Log channel With __/setlogchannel__")
    	return

    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title=f"Kicked {member}",
            description=f"{interaction.user.mention} kicked {member.mention}\n(bot: {member.bot})\nReason: {reason}",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {interaction.user}")
        await interaction.response.send_message(embed=embed)
        log = bot.get_channel(log_channel)
        await log.send(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to kick this member.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a user or bot from the server")
@app_commands.describe(member="Select a member (can be a bot)", reason="Reason for banning")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ You don't have permission to ban members.", ephemeral=True)
        return

    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title=f"Banned {member}",
            description=f"{interaction.user.mention} banned {member.mention}\nReason: {reason}",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Requested by {interaction.user}")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to ban this member.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

@bot.tree.command(name="setlogchannel", description="Setup the log channel")
@app_commands.describe(logchannelid="Channel ID for logging actions")
async def setlogchannel(interaction: discord.Interaction, logchannelid: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You don't have permission to setup.", ephemeral=True)
        return

    try:
        id = int(logchannelid)
        global log_channel
        log_channel = id
        await interaction.response.send_message(f"✅ Logs have been set to <#{id}>")
    except:
        await interaction.response.send_message("❌ Invalid channel ID.", ephemeral=True)

bot.run(process.env.token)
