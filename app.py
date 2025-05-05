from flask import Flask, redirect, url_for, render_template, request, session, flash
import sqlite3
app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


def initialise_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
        )''')

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        task_name TEXT,
        due_date TEXT,
        completed BOOLEAN DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
    conn.commit()
    conn.close()







initialise_db()

def get_db_connection():
    # we are connecting to our database and return a variable
    # that is linked to the db and can be used 
    db = sqlite3.connect('app.db')
    cursor = db.cursor()
    return db, cursor

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        db, cursor = get_db_connection()
        username = request.form["username"]
        password = request.form["password"]
        # send to db 
        cursor.execute('''
            INSERT OR IGNORE INTO users(username,password)
            VALUES(?,?)''', (username, password))
        
        db.commit()

        # flash signup successful
        
        return redirect(url_for("login"))
    
    return render_template('signup.html')





@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if that username and password is actually in the system 
        # if yes then go to do list and populate it with whatever is linked to that user
        db, cursor = get_db_connection()
        user_username = request.form["username"]
        user_password = request.form["password"]

        # this is already checking if that username and password is inside
        # if user_info i blank then we have something to work with
        print("issue 1")
        cursor.execute('''
            SELECT username,password FROM users
            WHERE username = ? AND password = ?
        ''', (user_username, user_password))
        print("issue 2")
        user_info = cursor.fetchall()
        # now compare the inputted info to the on in db
        # if it doesnt match they must go back to login 
        # we must write incorrect somewhere
        # if its correct then we go to to do list
        if len(user_info) == 0:
            # flash unsuccessful
            return render_template("login.html")

        else:
            # flash successful
            return redirect(url_for("todolist"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@app.route("/todolist")
def todolist():
    return render_template("todolist.html")




if __name__ == "__main__":
    app.run(debug=True)
