from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

PUBLIC_PASSWORD = "CoreLab$123"


@app.route("/", methods=["GET", "POST"])
def panel():

    message = ""

    if request.method == "POST":

        password = request.form.get("password")
        token = request.form.get("token")

        if password != PUBLIC_PASSWORD:
            message = "Invalid Password"

        else:
            if token:

                # Restart bot with token environment variable
                env = os.environ.copy()
                env["DISCORD_TOKEN"] = token

                subprocess.Popen(
                    ["python", "bot/bot.py"],
                    env=env
                )

                message = "Bot Started Successfully"

    return render_template("index.html", message=message)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
