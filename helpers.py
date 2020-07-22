import os
import requests
import urllib.parse
import calendar
import datetime

from flask import redirect, render_template, request, session
from functools import wraps
import pandas as pd

# this function was borrowed from CS50 finance distribution code
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#formats date and time nicely for user viewing
def dateFormat(s):
    if s == "Not available": #in the login function some datetimes are "Not available"
        return s
    else:
        mon = int(s[0:2])
        day = s[3:5]
        year = s[6:10]
        time = s[11: 16]
        month = calendar.month_name[mon]
        if int(s[11:13]) >= 13:
            return month + " " + day + ", " + year + " at " + str(int(s[11:13]) - 12) + ":" + s[14:16] + "PM"
        elif int(s[11:13]) == 12: #if 12pm
            return month + " " + day + ", " + year + " at " + s[11:16] + "PM"
        elif int(s[11:13]) >= 10 and int(s[11:13]) < 12:
            return month + " " + day + ", " + year + " at " + s[11:16] + "AM"
        else:
            return month + " " + day + ", " + year + " at " + s[12:16] + "AM"

# turns 1s and 0s into confirmed and unconfirmed for user display
def confirmed(n):
    if n == 1:
        return "Confirmed"
    else:
        return "Unconfirmed"

#it must be a string formatted in this way: s= "%m/%d/%Y %H:%M"
#you can use strftime to make it if you already have a datetime object
#or you can implement a similar function to this one
def roundtime(s, roundTo=30*60):
   s = datetime.datetime.strptime(s, "%m/%d/%Y %H:%M")
   seconds = (s.replace(tzinfo=None) - s.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return (s + datetime.timedelta(0,rounding-seconds,-s.microsecond)).strftime("%m/%d/%Y %H:%M")

#it takes a string in the same format as roundtime and the number of hours of the shift
def shifttime(s, h, m):
   s = datetime.datetime.strptime(s, "%m/%d/%Y %H:%M")
   return (s + datetime.timedelta(hours=h, minutes=m)).strftime("%m/%d/%Y %H:%M")

