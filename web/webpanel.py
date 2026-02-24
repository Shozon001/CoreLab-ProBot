from flask import Flask, render_template
import os
import subprocess

app = Flask(__name__)

TOKEN = os.getenv("DISCORD_TOKEN")

@app.route("/")
def home():
    return render_template("index.html")


def start_bot():
    if TOKEN:
        subprocess.Popen(["python", "bot/bot.py"])


if __name__ == "__main__":

    # Start bot process
    start_bot()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
