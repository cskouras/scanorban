# Scan Or Ban Design Implementation

## link to screencast: https://youtu.be/aO1mdPHHjVY

## Design Overview
We hoped to design a clear, well-organized website so that the user experience was as streamlined as possible.
To do this we designed multiple HTML pages with a CSS file, stored data in three SQLite tables, and connected all of these files together in application.py


### Installing

If you are using the IDE, then all the required pyhton packages are already installed. So you can just go to the directory and run flask.
Otherwise, if you need to host the site on a local server, lookup https://topherpedersen.blog/2019/12/28/how-to-setup-a-new-flask-app-on-a-mac/
to setup flask and create a virtual environment, then use "pip install" to install the various required packages.

Also, you can lookup at our GIT directory https://github.com/fabrisera/finalproject to clone the project into a local directory, and see all the commits!

### DATABASE DESIGN
Below are the three tables in which we stored information about our users, the rooms, and the bookings of rooms by users.

CREATE TABLE "users" (
        "user_id"       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "password_hash" TEXT NOT NULL,
        "email" TEXT NOT NULL,
        "admin" TEXT
);

CREATE TABLE "rooms" (
        "room_id"       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "room_name"     TEXT NOT NULL UNIQUE,
        "size"  NUMERIC,
        "location"      TEXT
);

CREATE TABLE "bookings" (
        "booking_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "user_id"       INTEGER,
        "broomid"       INTEGER,
        "start" SMALLDATETIME,
        "end"   SMALLDATETIME,
        "confirmed"     BOOLEAN
);

## QR CODE COMPONENT
Ideally, each room that is available for a reservation will have a unique QR code on iPad display inside the room for students to scan with their phones
We generated 7 QR codes using https://www.qr-code-generator.com/, each corresponding to one of the 7 rooms in our database.
Each QR code links to the URL of our website, followed by "/confirm?roomID=(integer 1 through 7)"
RoomID is a URL parameter, and it's value is associated with the room that it is attached to
Scanning the QR code will take you to the confirm page, where you can either book this room or confirm the previous booking of this room after logging in


### HTML FILES
The design of our website involved creating multiple HTML files (listed below) for each distinct feature of the website,
with each HTML file extending layout.html to ensure that certain feautures of our website design (such as the header and footer) stayed constant on each page of the website.

Below are the files:

layout.html

account.html
availabilities.html
book.html
bookings.html
code.html
confirm.html
directbook.html
index.html
login.html
padview.html
register.html
scan.html
layout.html


## Styling
We made one CSS file, styles.css, which is linked in the layout.html file, that contains the majority of our styling features.
We also used some elements of Bootstrap to enhance the appearance of certain features of the website, such as the tables displayed.


## Built With

Flask
Python
Jquery
CSS
HTML
Jinja




## Flask Functions
Below is a list of each function we implemented in application.py with its description.

Login
- Shows the login page via GET
- Does two actions via POST
    1)just logs the user in if the username and password (hashed) are correct if it is beign reached regularly
    2)also checks whether the QRcode correspondant room either needs to be confirmed (as it has already been booked by the user) or
    allows the user to reserve it for up to the next two hours (or less dependent on the availability of the room)


Logout
- Logs user out


Register
- shows register.html via GET, then via POST
- registers the users verifying though REGEX (implemented in the register.html) whether the username is an email and the passwords match and confirm

Book
- if request via "POST"
  - checks if book was accessed through a QR code scan, and if so, insert a new booking at the current time for the room associated with the QR code
  - if not, this means it was accessed through the website book option. If so:
     - check for validity of input, then query the rooms and bookings table for rooms that meet the user's requirements (for time, date, and size)
     - user option to book one of these rooms with a dropdown menu
     - generate an html page, availibilities.html, with all of the rooms that are available

- if request via "GET"
 - if there is a URL parameter called roomID, store it in a global variable
 - regardless render the template for book.html


Availabilities
- if request via "POST" - this means the user has just selected a room to book
   - insert the bookings information into the bookings database


Bookings
- if accessed via GET
  - query the database for upcoming room bookings (from today and onward)
  - pass this information along to the bookings.html page
- if accessed via POST
  - this means a cancelation has occured
  - delete the entry from the bookings table

Account:
- Allows user to change password if desired
- if accessed through "get", render account.html
- if accessed through "post":
  - undergoes several checks to make sure user input is proper
  - updates the users table with the hash of the new password

Direct Book
- if accessed via POST
- takes from the directbook page the user imput for booking
- books the specific room with status confirmed, as it was booked in person
- books the room for the specific time inserted by the user

Confirm
- if accessed through "get", this means the method was accessed through QR code scanning
- each QR code has a unique

Padview
- this is the function that is used by the iPads in order to display the room scheduling of a specific room as well as its QR code
- if accessed via post
  - queries the bookings database for all the bookings of a specific room

## helpers.py
Helpers.py consisted of functions that helped us to avoid clutter in application.py.
Two of the functions, dateFormat and confirmed, were filters that helped with user display on jinja.


## Authors

Carlo Kobe
Calliste Skouras
Fabrizio Serafini