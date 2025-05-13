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
        username TEXT ,
        password TEXT
        )''')

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_name TEXT,
        due_date TEXT,
        completed BOOLEAN DEFAULT 0,
        category TEXT,
        FOREIGN KEY(category) REFERENCES category(category_name),
        FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
    
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS category(
        category_name TEXT UNIQUE
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
        flash("Signed up successfully!", "info")
        return redirect(url_for("login"))
    
    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if that username and password is actually in the system 
        # if yes then go to do list and populate it with whatever is linked to that user
        db, cursor = get_db_connection()
        username = request.form["username"]
        session['username'] = username
        password = request.form["password"]

        # this is already checking if that username and password is inside
        # if user_info i blank then we have something to work with

        cursor.execute('''
            SELECT username,password FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))
 
        user_info = cursor.fetchall()
        # now compare the inputted info to the on in db
        # if it doesnt match they must go back to login 
        # we must write incorrect somewhere
        # if its correct then we go to to do list
        if len(user_info) == 0:
            # flash unsuccessful
            flash("Login unuccessful. Try again", "info")
            return render_template("login.html")

        else:
            # flash successful
            session["loggedin"] = True
            return redirect(url_for("todolist", username=username))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out", "info")
    return redirect("/")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@app.route("/todolist", methods=["GET", "POST"])
def todolist():
    username = request.args.get('username')
    db, cursor = get_db_connection() # we connect to our sever
    user_task = [] # an empty list which we will feed

    cursor.execute('''
    SELECT id FROM users 
    WHERE username = ?
    ''', (username,))

    db_id = cursor.fetchone()
    posted_correct = True
   
    # if no information is given it has to flash then render template?  
    if request.method == "POST":
        # we have to fetch the users unique ID so that the task is linked to a user
        user_task.append(db_id[0])
    
        user_task.append(request.form["task-name"])     
        user_task.append(request.form["deadline"])
        user_task.append(request.form["dropdown"])

        for i in range(1,len(user_task)):
            print(user_task[i])
            print(len(user_task[i]))
            if len(user_task[i]) == 0:
                flash("You have not filled in all the information")
                cursor.execute('''
                SELECT task_name, completed FROM tasks
                WHERE user_id = ?
                ''', db_id)
                all_user_tasks = cursor.fetchall()
                return render_template("todolist.html", username=username, tasks=all_user_tasks, loggedin=session.get('loggedin', True))
                
        else:
            user_task = tuple(user_task)
            cursor.execute('''
            INSERT INTO tasks(user_id, task_name, due_date, category)
            VALUES(?,?,?,?)             
            ''', user_task)
            db.commit()

        cursor.execute('''
        SELECT task_name, completed FROM tasks
        WHERE user_id = ?
            ''', db_id)
        all_user_tasks = cursor.fetchall()
        return render_template("todolist.html", username=username, tasks=all_user_tasks, loggedin=session.get('loggedin', True))
       
     # now every time we post it has to display

    cursor.execute('''
    SELECT id FROM users 
    WHERE username = ?
    ''', (username,))

    db_id = cursor.fetchone()
    print(db_id)
    cursor.execute('''
    SELECT task_name, completed FROM tasks
    WHERE user_id = ?
        ''', db_id)
    
    user_tasks = cursor.fetchall()
    db.close()
    print(user_tasks)
    # we're rendering the template with the information. Should be able to {{}} it in our html file
    return render_template("todolist.html", username=username, tasks=user_tasks, loggedin=session.get('loggedin', True))


@app.route("/delete_task", methods=["GET", "POST"])
def delete_task():
    username = session.get('username')
    return  redirect(url_for("todolist", username=username))

@app.route("/edit_task", methods=["GET", "POST"])
def edit_task():
    username = session.get('username')
    return redirect(url_for("todolist", username=username))


if __name__ == "__main__":
    app.run(debug=True)
