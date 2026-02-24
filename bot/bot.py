import discord
from discord.ext import commands
import aiohttp
import re
import json
import os

# Load Token
TOKEN = os.getenv("DISCORD_TOKEN")

API_BASE = "https://api.ip2location.io/?key=2BA7BD8AEF5682B12FD4B98CC3F19D4F&ip="

DEVELOPER_NAME = "MD Shozon Ahamed Shehab"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# IP Validation
def is_valid_ip(ip):
    return re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip)


# Bot Ready Event
@bot.event
async def on_ready():
    print("Bot Online:", bot.user)

    await bot.change_presence(
        activity=discord.Game(name=f"Developed by {DEVELOPER_NAME}")
    )


# ==========================
# IP Lookup Command
# ==========================
@bot.command()
async def ip(ctx, ip_address: str):

    if not is_valid_ip(ip_address):
        await ctx.send("❌ Invalid IP Format")
        return

    url = API_BASE + ip_address

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = json.loads(await response.text())

    if "country_name" not in data:
        await ctx.send("❌ API Error")
        return

    embed = discord.Embed(
        title="IP Lookup Result",
        description=data.get("ip"),
        color=0x2ecc71
    )

    embed.add_field(name="Country", value=data.get("country_name"), inline=True)
    embed.add_field(name="Region", value=data.get("region_name"), inline=True)
    embed.add_field(name="City", value=data.get("city_name"), inline=True)
    embed.add_field(name="ISP", value=data.get("isp"), inline=True)
    embed.add_field(name="Fraud Score", value=data.get("fraud_score"), inline=True)

    lat = data.get("latitude")
    lon = data.get("longitude")

    if lat and lon:
        embed.add_field(
            name="Map",
            value=f"https://www.google.com/maps?q={lat},{lon}",
            inline=False
        )

    await ctx.send(embed=embed)


# ==========================
# Developer Command
# ==========================
@bot.command(name="dev")
async def dev(ctx):

    embed = discord.Embed(
        title="👨‍💻 Developer Information",
        color=0x3498db
    )

    embed.add_field(name="Name", value="MD Shozon Ahamed Shehab", inline=False)
    embed.add_field(name="Age", value="20+", inline=True)
    embed.add_field(name="Nationality", value="Bangladeshi", inline=True)
    embed.add_field(name="Relationship", value=" Single 💔", inline=False)
    embed.add_field(name="Phone", value="+8809658225161", inline=False)
    embed.add_field(name="Discord Profile", value="https://discord.com/users/825450245005639702", inline=False)
    embed.add_field(name="Discord Server", value="https://discord.gg/E99grsqtGm", inline=False)

    embed.set_footer(text="Official Bot Developer")

    await ctx.send(embed=embed)


# Run Bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("DISCORD_TOKEN environment variable not found")
