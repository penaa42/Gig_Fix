from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.musician_model import Musician
from flask_app.models.band_model import Band
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

###################################################################################
# 1) home html
@app.route('/')
def home():
    return render_template('home.html')

# home html
@app.route('/musician')
def musician_index():
    return render_template('musician_index.html')

# 2) create new musician    8) validate musician     html request.form;
@app.route('/musician/register', methods = ['POST'])
def musician_register():

    if not Musician.validate_musician(request.form):
        print('FAILED MUSICIAN VALIDATE')
        return redirect('/musician')
#   saving the hashed password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
#   print(pw_hash)

#   recreating new dict with the upated hashed password
    pw_hash_data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "genre" : request.form['genre'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "experience" : request.form['experience'],
        "description" : request.form['description'],
        "instrument" : request.form['instrument'],
        "email" : request.form['email'],
        "password" : pw_hash
    }

#   call classmethod with info from request.form(dict) plus new hashed password w/bcrypt
    musician_id = Musician.create_musician(pw_hash_data)
#   have musician_id available throughout
    session['musician_id'] = musician_id

    session['first_name'] = request.form['first_name']
    print('------------MUSICIAN SESSION FIRST NAME IN REGISTER-----------', session['first_name'])

    return redirect('/profile')


@app.route('/musician/login', methods = ['POST'])
def musician_login():
    email_dict = {
        'email' : request.form['email']
    }

    # should either be a class of the User (if found) or False if it doesn't exist
    musician_in_db = Musician.find_musician_email(email_dict)
    if not musician_in_db:
        flash('Invalid email/password!', 'category2')
        return redirect('/musician')

    if len(request.form['password']) < 8:
        flash('Invalid email/password!', 'category2')
        return redirect('/musician')
    
    # checking if the passwords match
    if not bcrypt.check_password_hash(musician_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash('Invalid Email/Password!', 'category2')
        return redirect('/musician')
    
    # if the passwords matched, we set the user_id into session
    session['musician_id'] = musician_in_db.id
    # allowing access to first name for login display
    session['first_name'] = musician_in_db.first_name

    return redirect('/profile')


@app.route('/profile')
def profile():
    return render_template('profile.html')



###########################################################################################################








































@app.route('/name of path/route goes here!', methods=['POST']) #Post request route
def rename1():
    return redirect('/route path goes here!')

@app.route('/dashboard')
def rename2():
    return render_template('Dashboard html page here!')