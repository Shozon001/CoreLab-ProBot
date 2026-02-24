from flask import Flask, render_template
import os
import threading
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# =======================
# Discord Bot Setup
# =======================

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start(TOKEN))


# =======================
# Flask Routes
# =======================

@app.route("/")
def home():
    return render_template("index.html")


# =======================
# Start Everything
# =======================

if __name__ == "__main__":
    # Start Discord bot in background thread
    threading.Thread(target=run_bot).start()

    # IMPORTANT: Render dynamic port fix
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
