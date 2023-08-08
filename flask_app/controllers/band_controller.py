from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.band_model import Band
from flask_app.models.musician_model import Musician
from flask_app.models.song_model import Song
from flask_bcrypt import Bcrypt

import pprint

bcrypt = Bcrypt(app)

# home html
@app.route('/band')
def band_index():
    return render_template('band_index.html')


# CREATE NEW BAND       VALIDATE BAND       html request.form
@app.route('/band/register', methods = ['POST'])
def band_register():

    if not Band.validate_band(request.form):
        print('FAILED BAND VALIDATE')
        return redirect('/band')
#   saving the hashed password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
#   print(pw_hash)

#   recreating new dict with the upated hashed password
    pw_hash_data = {
        "name" : request.form['name'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "email" : request.form['email'],
        "password" : pw_hash
    }

#   call classmethod with info from request.form(dict) plus new hashed password w/bcrypt
    band_id = Band.create_band(pw_hash_data)
#   have band_id available throughout
    session['band_id'] = band_id

    session['name'] = request.form['name']
    print('------------BAND SESSION NAME IN REGISTER-----------')
    pprint.pprint(session['name'])

    return redirect('/dashboard')


@app.route('/band/login', methods = ['POST'])
def band_login():
    email_dict = {
        'email' : request.form['email']
    }

    # should either be a class of the User (if found) or False if it doesn't exist
    band_in_db = Band.find_band_email(email_dict)
    if not band_in_db:
        flash('Invalid email/password!', 'category2')
        return redirect('/band')

    if len(request.form['password']) < 8:
        flash('Invalid email/password!', 'category2')
        return redirect('/band')
    
    # checking if the passwords match
    if not bcrypt.check_password_hash(band_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash('Invalid Email/Password!', 'category2')
        return redirect('/band')
    
    # if the passwords matched, we set the user_id into session
    session['band_id'] = band_in_db.id
    # allowing access to first name for login display
    session['name'] = band_in_db.name

    return redirect('/dashboard')


# DASHBOARD: DISPLAY ALL MUSICIANS
@app.route('/dashboard')
def dashboard():
    # if not 'band_id' in session:
    #     print('FAILED DASHBOARD SESSION VALIDATION')
    #     return redirect('/band')

    return render_template('dashboard.html', musicians = Musician.get_all())


@app.route('/profile/<int:musician_id>')
def view_profile(musician_id):

    # musician_id = session['musician_id']

# DASHBOARD: DISPLAY ALL SONGS WITH MUSICIAN
    # if not 'user_id' in session:
    #     print('FAILED DASHBOARD SESSION VALIDATION')
    #     return redirect('/')

    # session['band_id'] = 

    id_data = {
        'id' : musician_id
    }

    musician = Musician.show_musician(id_data)

    print('---------------MUSICIAN INFO PASSED TO HTML---------------')
    pprint.pprint(musician)

    # songs = Song.get_songs_w_musician()

    return render_template('profile.html', musician = musician, songs = Song.get_songs_w_musician())
###########################################################################################################


@app.route('/band/requests')
def band_requests():
    
    
    return render_template('band_request.html')































