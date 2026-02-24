from flask import Flask, render_template, request
import subprocess
import os
import signal

app = Flask(__name__)

PUBLIC_PASSWORD = "CoreLab$123"

bot_process = None


@app.route("/", methods=["GET", "POST"])
def panel():

    global bot_process

    message = ""

    if request.method == "POST":

        password = request.form.get("password")
        token = request.form.get("token")
        action = request.form.get("action")

        if password != PUBLIC_PASSWORD:
            message = "Invalid Password"
            return render_template("index.html", message=message)

        # Stop Bot
        if action == "stop":

            if bot_process:
                bot_process.terminate()
                bot_process = None

            message = "Bot Stopped"

        # Start Bot
        elif action == "start":

            if token:
                env = os.environ.copy()
                env["DISCORD_TOKEN"] = token

                bot_process = subprocess.Popen(
                    ["python", "bot/bot.py"],
                    env=env
                )

                message = "Bot Started"

    return render_template("index.html", message=message)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
