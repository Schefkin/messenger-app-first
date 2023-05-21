import os
from functools import wraps

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# configure app
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///table.db")

# login requiered decorator maybe later rewrite to functions file
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# flask application forces the client to always request a fresh version of the resource from the server
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response  

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":
        # gets the text that the user put into the form
        user_input = request.form.get('input')
        # print(user_input)
        
        # checks if the username is in the users database
        check_list = db.execute('SELECT EXISTS(SELECT 1 FROM users WHERE username = ?)', user_input)
        check = check_list[0]
        

        if 1 in check.values():
            print('nice')
            # I need to check if the name already exists in the table or not
            whole_list = db.execute('SELECT name FROM friends WHERE id = ?;', session["user_id"])
            print(whole_list)

            # checks if the user input is already in database
            for dict in whole_list:
                if user_input in dict['name']:
                    return render_template("index.html")
                

            # checks for my current accounts name
            my_current_name_list = db.execute('SELECT username FROM users WHERE id = ?', session["user_id"])
            my_current_name = my_current_name_list[0]['username']

            # checks whether user inputted his own name
            if user_input == my_current_name:
                return render_template("index.html")


            # adds the user to my friends list from "my prespective"
            db.execute('INSERT INTO friends (id, name) VALUES (?, ?);', session["user_id"], user_input)


            # checks for id of the users I just added
            added_user_id_list = db.execute('SELECT id FROM users WHERE username = ?', user_input)
            added_user_id = added_user_id_list[0]['id']

            

            # adds me to the users friend list from "his prespective"
            db.execute('INSERT INTO friends (id, name) VALUES (?, ?);', added_user_id, my_current_name)


            # selects all friends I currently have
            # friend_list = db.execute('SELECT name FROM friends WHERE id = ?', session["user_id"])

            return render_template("index.html")


        # if inputted name is not found in the users database then dont do anything
        elif 0 in check.values():
            print('L')
            return render_template("index.html")




    else:
        print('yo')

        
        return render_template("index.html")

  
@app.route("/friends", methods=["GET", "POST"])
@login_required
def friends():

    friend_list = db.execute('SELECT name FROM friends WHERE id = ?', session["user_id"])

    if request.method == "POST":
        # gets the value that was selected from the friends page list
        my_value = request.form.get('friend_name')
        
        # stores value in the session
        session['my_value'] = my_value

        # returns cool link + my_value nice job me
        return redirect("/messages")
    else:
        return render_template("friends.html", friend_list=friend_list)








@app.route("/messages", methods=["GET", "POST"])
@login_required
def messages():
    # retrieves my_value variable from the session so it can be used inside this function
    my_value = session.get('my_value')  # my_value is the name of the friend selected
    print(my_value)
    message = request.form.get('message_itself') # gets the string of the message that was submitted thru form

    # Checks for my current name
    my_current_name_list = db.execute('SELECT username FROM users WHERE id = ?', session["user_id"])
    my_current_name = my_current_name_list[0]['username']
    print(my_current_name)  

    # selects all my previous messages with the person
    previous_messages = db.execute('SELECT sender, recipient, message FROM messages WHERE (sender = ? OR sender = ?) AND (recipient = ? OR recipient = ?) ORDER BY timestamp;', my_current_name, my_value, my_current_name, my_value)
    
    if request.method == "POST":

        

        # checks if the message even exists and the user just didn't type ''
        if message:
            
            print(message)
            print(previous_messages)

            db.execute('INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)', my_current_name, my_value, message)

            return redirect("/messages")
            # return render_template("messages.html", my_current_name=my_current_name, my_value=my_value, previous_messages=previous_messages)
        
        

        # if user typed '' do nothing basically
        else:
            return redirect("/messages")
            # return render_template("messages.html", my_current_name=my_current_name, my_value=my_value, previous_messages=previous_messages)

    else:
        return render_template("messages.html", my_current_name=my_current_name, my_value=my_value, previous_messages=previous_messages)











@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        reg_username = request.form.get('username')
        reg_pass = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not request.form.get("username"):
            return render_template('register.html')

        elif not request.form.get("password"):
            return render_template('register.html')

        elif not request.form.get("confirmation"):
            return render_template('register.html')

        people = db.execute('SELECT username FROM users')
        existing_usernames = [person['username'] for person in people]

        if reg_username in existing_usernames:
            return render_template('register.html')

        if reg_pass == confirmation:
            hashed_pass = generate_password_hash(reg_pass)
            db.execute('INSERT INTO users (username, hash) VALUES(?, ?)', reg_username, hashed_pass)
            return redirect("/")
        else:
            return render_template('register.html')

    else:
        return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html") # apology

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html") # apology

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html")  # apology

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

print('hello')