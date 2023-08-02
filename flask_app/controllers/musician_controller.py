from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.rename_model import Rename #importing the class here
#There will be other imports need depending what you're trying to use in this file
#You will also need a bycrypt import (we will introduce this week 5)


@app.route('/') #Get request for 127.0.0.1:5000
def home():
    return render_template('index.html')

@app.route('/name of path/route goes here!', methods=['POST']) #Post request route
def rename1():
    return redirect('/route path goes here!')

@app.route('/dashboard')
def rename2():
    return render_template('Dashboard html page here!')