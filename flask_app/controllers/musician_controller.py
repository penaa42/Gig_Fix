from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.musician_model import Musician
from flask_app.models.band_model import Band
from flask_app.models.song_model import Song
from flask_app.models.chart_model import Chart
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt

import uuid as uuid
import os
import pprint

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

    print('-------CREATE MUSICIAN FORM DATA--------')

    if not Musician.validate_musician(request.form):
        print('FAILED MUSICIAN VALIDATE')
        return redirect('/musician')

#   saving the hashed password

    print('------PICTURE NAME------')
    # pprint.pprint(profile_pic)

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
        "availability" : request.form['availability'],
        "email" : request.form['email'],
        "password" : pw_hash
    }

#   call classmethod with info from request.form(dict) plus new hashed password w/bcrypt
    musician_id = Musician.create_musician(pw_hash_data)
#   have musician_id available throughout
    session['musician_id'] = musician_id

    session['first_name'] = request.form['first_name']
    print('------------MUSICIAN SESSION FIRST NAME IN REGISTER-----------')
    pprint.pprint(session['first_name'])

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
    session['last_name'] = musician_in_db.last_name

    return redirect('/profile')


@app.route('/profile')
def profile():
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')

    musician_id = session['musician_id']

    id_data = {
        'id' : musician_id
    }

    musician = Musician.show_musician(id_data)

    print('---------------MUSICIAN INFO PASSED TO HTML---------------')
    pprint.pprint(musician)

    return render_template('profile.html', musician = musician, songs = Song.get_songs_w_musician())

###########################################################################################################
@app.route('/profile/edit/<int:musician_id>')
def profile_edit(musician_id):
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')

    musician_id = session['musician_id']

    id_data = {
        'id' : musician_id
    }

    musician = Musician.show_musician(id_data)

    print('---------------MUSICIAN INFO PASSED TO HTML---------------')
    pprint.pprint(musician)

    return render_template('profile_edit.html', musician = musician)


@app.route('/profile/update', methods = ['POST'])
def update_profile():

    musician_id = session['musician_id']

    print('-------CHECK BEFORE USER UPDATE VALIDATE------------')

    if not Musician.validate_musician_update(request.form):
        print("FAILED UPDATE MUSICIAN VALIDATION")
        return redirect(f'/profile/edit/{musician_id}')

    id_data = {
        'id' : musician_id
    }

    musician = Musician.show_musician(id_data)

    print('---------------MUSICIAN INFO PASSED TO HTML---------------')
    pprint.pprint(musician)
    print('--------PASSWORD PULLED FROM SHOW MUSICIAN-----------')
    pprint.pprint(musician.password)

#   setting up dict for query from request.form
    update_data = {
        'id' : session['musician_id'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'genre' : request.form['genre'],
        'city' : request.form['city'],
        'state' : request.form['state'],
        'experience' : request.form['experience'],
        'instrument' : request.form['instrument'],
        'availability' : request.form['availability'],
        'description' : request.form['description'],
    }

    print('-------------UPDATE SHOW DATA-------------')
    pprint.pprint(update_data)

#   call update method
    Musician.update_profile(update_data)

    return redirect('/profile')

########################################################
# DELETE SONG        input: html profile, view song, song_id
# DASHBOARD
@app.route('/profile/delete_song/<int:song_id>')
def delete_song(song_id):

    print('----------CHECKING SHOW DELETE ID------------')
    pprint.pprint(song_id)

    delete_data = {
        'id' : song_id
    }

    Song.delete_song(delete_data)

    return redirect('/profile')

@app.route('/profile/requests/<int:musician_id>')
def request_page(musician_id):
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')

    print('----CHECKING FOR MUSICIAN ID IN GIG REQUESTS----')
    pprint.pprint(musician_id)

    musician_id_dict = {
        'id' : session['musician_id']
    }

    print('----MUSICIAN ID DICT-----')
    pprint.pprint(musician_id_dict)

    return render_template('musician_request.html', bands = Musician.get_all_band_w_musician(musician_id_dict))


########################################################
# DELETE BAND REQUEST        input: html musician_request, band_id musician_id
@app.route('/profile/requests/decline/<int:musician_id>/<int:band_id>')
def delete_band_request(musician_id, band_id):

    print('----------CHECKING JOIN DELETE ID------------')
    print('---MUSICIAN_ID----')
    pprint.pprint(musician_id)

    print('----BAND_ID----')
    pprint.pprint(band_id)

    delete_data = {
        'musician_id' : musician_id,
        'band_id' : band_id
    }

    print('-------DELETE DATA W/ MUSICIAN AND BAND------')
    pprint.pprint(delete_data)
    Musician.delete_band_w_musician(delete_data)

    return redirect(f'/profile/requests/{musician_id}')


@app.route('/profile/requests/view/chart/<int:musician_id>/<int:band_id>')
def view_band_chart(musician_id, band_id):
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')

    print('------MUSICIAN ID FOR CHART PULL------')
    print(musician_id)

    print('------BAND ID FOR CHART PULL------')
    print(band_id)

    show_data = {
        'id' : band_id
    }

    band_charts = Chart.profile_view_charts(show_data)

    print('----RETURN FROM CHART MODEL----')
    pprint.pprint(band_charts)

    musician_id_dict = {
        'id' : session['musician_id']
    }

    print('----BAND NAME FROM CHARTS------')
    band_name = Band.show_band(show_data)
    pprint.pprint(band_name)

    return render_template('musician_request.html', charts = band_charts, bands = Musician.get_all_band_w_musician(musician_id_dict), band_name = band_name)


@app.route('/profile/upload/image_page')
def upload_image_page():
    print('---MADE IT TO UPLOAD PAGE-----')

    return render_template('upload_image.html')


@app.route('/profile/add/image', methods = ['POST'])
def add_image():
    print('-----MADE IT TO UPLOAD ROUTE------')

    print('----PROFILE PIC REQUEST FORM----')
    print(request.files)

    # image
    profile_pic = request.files['profile_pic']
    print('------PROFILE_PIC------')
    print(profile_pic)

    #image name/secure filename
    pic_filename = secure_filename(profile_pic.filename)
    print('------PIC_FILENAME------')
    print(pic_filename)

    if not Musician.validate_profile_img(request.files):
        print('FAILED PROFILE PICTURE VALIDATE')
        flash('File upload failed, please try again.')
        return redirect('/profile/upload/image_page')

    #multiple same file names
    #set uuid
    pic_name = str(uuid.uuid1()) + "_" + pic_filename
    print('-----PROFILE PIC NAME------')
    print(pic_name)

    app_root = os.path.dirname(os.path.abspath(__file__))
    trim_app_root = app_root.split("controllers")
    print(trim_app_root)

    UPLOAD_FOLDER = os.path.join(trim_app_root[0], 'static', 'assests', 'img', 'profile')
    print('-----DIR_NAME----')
    print(app_root)
    print(UPLOAD_FOLDER)

    test_path = os.path.join(UPLOAD_FOLDER, pic_name)
    print('----TEST PATH FOR PIC------')
    print(test_path)

    # save image
    profile_pic.save(os.path.join(UPLOAD_FOLDER, pic_name))

    #set pic_name string to file
    profile_pic = pic_name

#   dict for musician_model UPDATE query
    pic_dict = {
        'id' : session['musician_id'],
        'profile_pic' : profile_pic
    }

    print('------PIC DICT------')
    pprint.pprint(pic_dict)

    Musician.add_image(pic_dict)

    return redirect('/profile')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
