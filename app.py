from flask import Flask, redirect, url_for, render_template, request, session, flash
import sqlite3
app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


def get_db_connection():
    cursor = sqlite3.connect('app.db')
    cursor.row_factory = sqlite3.Row
    return cursor

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = get_db_connection()
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username,password)).fetone()
        cursor.close()

        if user:
            return redirect(url_for("todolist"))


    return redirect(url_for("login")) #should return to sign up page


@app.route("/todolist")
def todolist():
    if "username" in session:
        return render_template("todolist.html")
    else:
        return "Not logged in"



if __name__ == "__main__":
    app.run(debug=True)
