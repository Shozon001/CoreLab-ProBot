from flask import Flask, render_template, request

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
                with open("token.txt", "w") as f:
                    f.write(token)

                message = "Bot Token Updated"

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)