from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form.get["username"]
        return redirect("/todolist")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@app.route("/submit", methods=["POST"])
def submit_form():
    username = request.form["username"]
    return redirect(url_for("todolist"))


@app.route("/todolist")
def todolist():

    return render_template("todolist.html")


if __name__ == "__main__":
    app.run(debug=True)
