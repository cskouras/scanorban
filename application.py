import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from flask import flash, render_template
from pytz import timezone
import pytz


from helpers import login_required, dateFormat, confirmed, shifttime, roundtime


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# filters defined in helper functions
#LEAVE AS IS
app.jinja_env.filters["dateFormat"] = dateFormat
app.jinja_env.filters["confirmed"] = confirmed


def isfree(start, halfs, room_id):

    start = roundtime(start)
    for i in range(halfs):
        #potential error here
        check = shifttime(start, 0, 30 * i + 1)
        dicti = db.execute("SELECT * FROM bookings WHERE broomid = :room_id AND \
            :check BETWEEN start AND end", room_id = room_id, check = check)
        if len(dicti) != 0:
            return i
    return (i + 1)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///room.db")


#http://127.0.0.1:5000/login?roomID=5

@app.route("/")
@login_required
def index():
    """ show the user's current bookings"""
    """ 'book a room' tab in the navigation bar """
    return redirect('/bookings')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    global roomID
    error = None
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        #check if roomID is not none to see whether you are from confirmation, if so
        #set the roomID variable and redirect to login
            if request.args.get('roomID') is not None:
                roomID = int(request.args.get('roomID'))
                print(roomID)
                return render_template("login.html")

            # Ensure username was submitted
            if not request.form.get("email"):
                error = "Must input email"
                return render_template("login.html", error=error)

            # Ensure password was submitted
            elif not request.form.get("password"):
               error = "Must input password"
               return render_template("login.html", error=error)


            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE email = :email",
                              email=request.form.get("email"))

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
                error = "Invalid username and/or password"
                return render_template("login.html", error=error)

            # Remember which user has logged in
            session["user_id"] = rows[0]["user_id"]

            #if you are logging in after coming from confirmation, then roomID is set, so you can execute the code and then reset roomID to none
            if roomID is not None:
                #print ("room id is not none")
                eastern = timezone('US/Eastern')
                time = datetime.datetime.now(eastern).strftime("%m/%d/%Y %H:%M")
                # confirm if the user is confirming an already booked room
                croom = db.execute('SELECT * FROM bookings WHERE user_id = :userid AND :datetime BETWEEN start AND end',\
                userid= session['user_id'], datetime = time)
                print(croom)

                # if there is not already a booked room by the user for this time
                if len(croom) == 0:
                #if it doesn't work try doing with a string before
                    temp = roomID
                    #roomID = request.args.get('roomID') #ID of the room the user wants to confirm
                    roomNameList = db.execute("SELECT room_name FROM rooms WHERE room_id = :roomID", roomID=roomID)
                    roomName = roomNameList[0]["room_name"]
                    # check if this room is currently booked already
                    eastern = timezone('US/Eastern')
                    start = datetime.datetime.now(eastern).strftime("%m/%d/%Y %H:%M")
                    mezze = int(isfree(start, 5, roomID))
                    if mezze == 0:
                        testtime = shifttime(time, 0, 31)
                        froom = db.execute('SELECT * FROM bookings WHERE user_id = :userid AND :datetime BETWEEN start AND end',\
                                            userid= session['user_id'], datetime = testtime)
                        if len(froom) != 0:
                            temp = roomID
                            db.execute('UPDATE bookings SET confirmed = :confirm WHERE booking_id = :bookingid',\
                                        bookingid= froom[0]['booking_id'], confirm=True)
                            roomID = None #reset roomID
                            return redirect("/")
                        else:
                            error = "sorry, this room is not available."
                            roomID = None
                            return render_template("confirm.html", roomID=temp, roomName=roomName, error=error)
                    else:
                        start = roundtime(start)
                        end = ["Not available"] * 5
                        for i in range(mezze):
                            end[i] = shifttime(start, 0, 30 * i + 30)
                        roomID = None
                        return render_template("directbook.html", roomID=temp, roomName=roomName, start=start, end=end)
                else:
                    temp = roomID
                    db.execute('UPDATE bookings SET confirmed = :confirm WHERE booking_id = :bookingid',\
                     bookingid= croom[0]['booking_id'], confirm=True)
                    roomID = None #reset roomID
                    return redirect("/")

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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    error = None
    if request.method == "POST":
        if not request.form.get("email"):  # if no email provided
            error = "must provide email"
            return render_template("register.html", error=error)

        # Ensure password was submitted
        elif not request.form.get("password"):  # if no password provided
            error = "must provide password"
            return render_template("register.html", error=error)

        elif not request.form.get("confirmation"):  # if no password confirmation
            error = "must provide password confirmation"
            return render_template("register.html", error=error)

        elif request.form.get("password") != request.form.get("confirmation"):
            error = "passwords must match"
            return render_template("register.html", error=error)

        # if all fields are submitted and passwords are the same

        # query database for pre-existing username
        rows = db.execute("SELECT * FROM users WHERE email = :email", email=request.form.get("email"))

        if len(rows) != 0:  # if username of this string already exists
            error = "username already exists"
            return render_template("register.html", error=error)
        else:
            db.execute("INSERT INTO users (password_hash, email) VALUES (:password, :email)",
                      password=generate_password_hash(request.form.get("password")), email=request.form.get("email"))
            return redirect("/")

    else:  # if GET
        return render_template("register.html")

datetimer = None
datetimer_end = None

@app.route("/book", methods=["GET", "POST"])
@login_required
def book():
    if request.method == "POST":
        #if booking a room through the book page (not QR code)
        global datetimer, datetimer_end
        date = str(request.form.get("date"))
        time = str(request.form.get("time"))

        # check if user has inputted a time that has already passed
        userDateTime = datetime.datetime.strptime(date + " " + time,"%m/%d/%Y %H:%M") #convert string to datetime object
        est = timezone('US/Eastern')
        userDateTimeAware = est.localize(userDateTime) #assign timezone to datetime object that the user inputed

        now = datetime.datetime.now(est)
        error = None

        if userDateTimeAware < now:
            error = "Error: you have inserted a date/time that has already passed. Please use this page to book a room in advance."
            return render_template("book.html", error=error)

        datetimer = date + " " + time
        datetimer_start = shifttime(datetimer, 0, 1)
        h = int(request.form.get("duration"))
        datetimer_end = shifttime(datetimer, h, 0)
        print(datetimer_end)
        size = int(request.form.get("size"))
        availabilities = db.execute("SELECT * FROM rooms WHERE NOT room_id IN (SELECT broomid FROM bookings WHERE :datetime_start BETWEEN start AND end)\
        AND NOT room_id IN (SELECT broomid FROM bookings WHERE \
        :datetime_end BETWEEN start AND end) AND room_id IN (Select room_id FROM rooms where size >= :size)", datetime_start=datetimer_start, datetime_end=datetimer_end, size=size)

        if len(availabilities) != 0: #if there are rooms that meet the date/time requirements
            return (render_template("availabilities.html", availabilities = availabilities))
        else:
            error = "Sorry, there are no rooms available in this time slot. Please find another time to reserve a room."
            return render_template("availabilities.html", availabilities = availabilities, error=error)
    else: #if GET
        return render_template("book.html")


@app.route("/availabilities", methods=["GET", "POST"])
@login_required
def availabilities():
    if request.method == "POST":
        roomName = request.form.get("value")
        # find the room id for the requested room
        roomIdList = db.execute("SELECT room_id FROM rooms WHERE room_name = :roomName", roomName=roomName)
        roomId = roomIdList[0]["room_id"]

        #insert this info into bookings table
        db.execute("INSERT INTO bookings (broomid, user_id, start, end) VALUES \
                (:room_id, :user_id, :start, :end)", room_id=roomId, user_id = session["user_id"], \
                start=datetimer, end=datetimer_end)
        return redirect("/")
    else:
        return render_template("availabilities.html")

roomID = None


@app.route("/bookings", methods =['GET', 'POST'])
@login_required
def bookings():
    if request.method == "GET":
        today = datetime.date.today()
        day = today.strftime("%m/%d/%y")
        #select for only upcoming room bookings
        bookings = db.execute("SELECT * FROM bookings JOIN rooms ON broomid = room_id WHERE user_id = :user_id AND start >= :start ORDER by start", user_id = session["user_id"], start = day)
        noBookings = None;
        #if there are no upcoming bookings
        if len(bookings) == 0:
            noBookings = "You have no upcoming bookings"
        return render_template("bookings.html", info = bookings, noBookings=noBookings )
    else: #if POST
         canc = request.form.get("cancelation")
         db.execute("DELETE FROM bookings WHERE booking_id = ?", canc)
         return redirect("/bookings")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("old_password"):
           error = "must provide original password"

        # Ensure password was submitted
        if not request.form.get("new_password"):
            error = "must provide new password"

        if not request.form.get("confirmation"):
           error = "must confirm new password"

        query = db.execute("SELECT password_hash from users where user_id = :uid", uid=session["user_id"])

        if len(query) != 1 or not check_password_hash(query[0]["password_hash"], request.form.get("old_password")):
            error = "not correct password"

        elif request.form.get("new_password") != request.form.get("confirmation"):
            error = "not correct password"

        new_hash = generate_password_hash(request.form.get("new_password"))

        # storing user
        execute = db.execute("Update users SET password_hash = :new_hash WHERE user_id = :uid", uid=session["user_id"], new_hash=new_hash)

        # Return Homepage
        return redirect("/book")
    else:
        return render_template("account.html")

@app.route("/directbook", methods=["GET", "POST"])
@login_required
def directbook():
    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")
        roomid = request.form.get("roomID")
        db.execute("INSERT INTO bookings (broomid, user_id, start, end, confirmed) VALUES \
                (:room_id, :user_id, :start, :end, :confirmed)", room_id=roomid, user_id = session["user_id"], \
                start=start, end=end, confirmed=True)
        return redirect("/")
    else:
        return redirect("/book")

@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    if request.method == "GET": #if accessed from QR code scan
        roomID = request.args.get('roomID') #ID of the room the user wants to confirm
        roomNameList = db.execute("SELECT room_name FROM rooms WHERE room_id = :roomID", roomID=roomID)
        roomName = roomNameList[0]["room_name"]
        # check if this room is currently booked already
        eastern = timezone('US/Eastern')
        start = datetime.datetime.now(eastern).strftime("%m/%d/%Y %H:%M")
        return render_template("confirm.html", roomID=roomID, roomName=roomName)

    else:
        return redirect('login?roomID=' + roomID)


@app.route("/padview", methods=["GET", "POST"])
def padview():
    if request.method == "POST":
        if not request.form.get("room"):
            error = "Must provide room name"

        room = request.form.get("room")
        today = datetime.date.today()
        day = today.strftime("%m/%d/%y")

        info = db.execute("SELECT * FROM bookings where broomid = (Select room_id from rooms where room_name = :room) AND start >= :start ORDER by start", room = room,  start = day)
        return render_template("code.html", room = room, info = info)
    else:
        return render_template("padview.html")


