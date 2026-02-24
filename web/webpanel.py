from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)

PUBLIC_PASSWORD = "CoreLab$123"

TOKEN_FILE = "token.txt"


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

                # Save token from panel
                with open(TOKEN_FILE, "w") as f:
                    f.write(token)

                # Restart bot
                subprocess.Popen(["python", "bot/bot.py"])

                message = "Bot Restarted Successfully"

    return render_template("index.html", message=message)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
