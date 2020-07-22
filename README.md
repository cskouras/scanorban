## Scan Or Ban Documentation

## link to screencast: https://youtu.be/aO1mdPHHjVY


## Background:
With Scan or Ban, we gave ourselves the task of optimizing the room booking experience when booking study rooms in spaces such as Cabot Library or the Smith Campus Center.

Specifically, our goal was to enable on-arrival bookings of rooms, as well as implement a function which requires users to confirm their bookings upon arrival.

These functions aim to address two inefficiencies we have noticed with the room booking application utilized by the Harvard Library System:
Many students book spaces that they do not end up needing, or book spaces for longer time frames than they need them.
Oftentimes students spontaneously occupy empty rooms but do not formally book them. This leads to awkward situations in which students get kicked out of the room by others who formerly reserved the space online knowing or not knowing that it was indeed occupied.

## Disclaimer
Although we would have liked to use the database owned by Harvard IT, we attempted to contact them, though they told us that the database could not be shared to students.
For this reason, the rooms database for the Scan or Ban website is simply a model of the study rooms that are available on the Harvard campus (our database has 7 rooms)


## Running the application
Scan or Ban is a python web application using flask.
In order to initiate the program, one must first move into the respective directory in one’s IDE, and subsequently initiate flask via a “flask run” command in the terminal.
A link will be generated, and clicking the link will take the user to the website.
Alternatively, users can access the website by scanning any one of the QR codes associated with a room.

## User experience
Upon clicking on the URL for our website’s homepage, a user is prompted to log in with an existing email and password.
If the user has not yet created an account, they should navigate to the top-right corner of the screen in the navigation bar,
where they can click on the register button and register a new email and password.
Once a new user has registered their account, they are redirected to the login page, where they can enter their new login credentials.

After logging in, the user is directed to the bookings page, which displays all of the user’s upcoming room bookings in a table format.
If the user has no upcoming bookings, the website should display, “you have no upcoming bookings.”

If the user wants to book a room ahead of time, they should navigate to the “Book” feature in the navigation bar.
Here, they are prompted to enter the desired date, time, and duration of their booking as well as the minimum number of seats they want the user to have.
The user then should click the button “Check Availabilities”.
If the user has entered a time that has already passed (in the Boston timezone), an error message is displayed, and the user is prompted to restart their booking selection.
Otherwise, clicking the “check availabilities” button will redirect users to the availabilities page.

The availabilities page displays all rooms that can be reserved given the requested time frame and size conditions.
A table displays information regarding the name and location of the room.
Furthermore, images of the available rooms are displayed.
Users can then choose the specific room they want to reserve using a drop-down menu, and finalize the booking by clicking the “Reserve” button.

Consequently, the user is redirected to the “bookings” page. This page also includes a function that enables the cancelation of specific future bookings.

Users are able to use the “account” function in order to change their password.
The last feature on the navigation bar is a logout button, where the user can log out of their account.

Not immediately visible on the web layout are the functions designed for enabling users to book or confirm a booking after arrival.
All spaces will be equipped with room specific QR codes.
Scanning the QR codes will enable the user to confirm their booking for that space, or make new reservations for the space.
The function dynamically recognizes if the user has a booking for that space close to the time the QR code is scanned.
If so, it asks the user if he/she wants to confirm the booking, and subsequently reroutes him to login.
After a successful login, the status of the specific booking will change to “Confirmed.”
If the user does not have a booking for the specific room close to the time of the scanning, the user is asked if he/she wants to make a new booking of the space at the current time.
Users are first rerouted to login, and then presented with a page enabling them to choose the length of the booking starting at the current time.

In addition to the functions targeted at users of the room bookings server, administrators are able to access the “padview” via the login page.
After choosing “access padview” administrators are able to choose the room.
The function then renders a page with the respective QR code for that room, as well as a table listing the upcoming bookings for the space.
This is meant to be displayed on the tablets outside of the specific rooms.


## Authors
Carlo Kobe
Fabrizio Serafini
Calliste Skouras


