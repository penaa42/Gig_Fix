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
    # pprint.pprint(request.form)
    # print('------TRYING TO SEE THE FORM DATA FOR PIC-------')
    # print(request.files['profile_pic'])

    if not Musician.validate_musician(request.form):
        print('FAILED MUSICIAN VALIDATE')
        return redirect('/musician')
#   saving the hashed password

    # if request.method == "POST":
    # the image itself
    # profile_pic = request.files['profile_pic']
    # # image name
    # pic_filename = secure_filename(profile_pic.filename)
    # # unique id
    # pic_name = str(uuid.uuid1()) + "_" + pic_filename
    # # save img
    # profile_pic.save(os.path.join(app.config['upload_folder'], pic_name))
    # #change to string to save to db
    # profile_pic = pic_name



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
        # "profile_pic" : profile_pic,
        # grab img name
        # pic_filename : ,
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

    # print('---------MUSICIAN ID-----------')
    # print(session['musician_id'])

    # print('---------MUSICIAN FIRST NAME-----------')
    # print(session['first_name'])
    
    # print('---------MUSICIAN LAST NAME-----------')
    # print(session['last_name'])
    # pprint(musician_in_db)


    return redirect('/profile')


@app.route('/profile')
def profile():
# DASHBOARD: DISPLAY ALL SONGS WITH MUSICIAN
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')
    # if not 'band_id' in session:
    #     print('FAILED MUSICIAN SESSION VALIDATION')
    #     return redirect('/')

    musician_id = session['musician_id']


    id_data = {
        'id' : musician_id
    }

    musician = Musician.show_musician(id_data)

    print('---------------MUSICIAN INFO PASSED TO HTML---------------')
    pprint.pprint(musician)

    # songs = Song.get_songs_w_musician()

    return render_template('profile.html', musician = musician, songs = Song.get_songs_w_musician())
###########################################################################################################

@app.route('/profile/edit/<int:musician_id>')
def profile_edit(musician_id):
    # DASHBOARD: DISPLAY ALL SONGS WITH MUSICIAN
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')
    # if not 'band_id' in session:
    #     print('FAILED MUSICIAN SESSION VALIDATION')
    #     return redirect('/')

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

    # update_info = {
    #     'password' : musician['password']
    # }


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
        # 'password' : musician.password

    }

    print('-------------UPDATE SHOW DATA-------------')
    pprint.pprint(update_data)

#   call update method
    Musician.update_profile(update_data)

    return redirect('/profile')



# @app.route('/profile/add_song')
# def add_song():
#     print('------ADD SONG-----')
#     return render_template('add_song.html')


# @app.route('/pofile/edit_song')
# def edit_song():

#     return render_template('edit_song.html')





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
    # Car.delete_car(delete_data)

    return redirect('/profile')


@app.route('/profile/requests/<int:musician_id>')
def request_page(musician_id):
    # DASHBOARD: DISPLAY ALL SONGS WITH MUSICIAN
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')
    # if not 'band_id' in session:
    #     print('FAILED MUSICIAN SESSION VALIDATION')
    #     return redirect('/')
# call a join request for musician and band
    print('----CHECKING FOR MUSICIAN ID IN GIG REQUESTS----')
    pprint.pprint(musician_id)

    musician_id_dict = {
        'id' : session['musician_id']
    }

    print('----MUSICIAN ID DICT-----')
    pprint.pprint(musician_id_dict)


# pass in band and chart query


# pass request to html

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
    # DASHBOARD: DISPLAY ALL SONGS WITH MUSICIAN
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')
    # if not 'band_id' in session:
    #     print('FAILED MUSICIAN SESSION VALIDATION')
    #     return redirect('/')
    print('------MUSICIAN ID FOR CHART PULL------')
    print(musician_id)

    print('------BAND ID FOR CHART PULL------')
    print(band_id)


    # Musician.view_band_charts()
    # print('---TESTING MUSICIAN VIEW CHART BAND_ID----')

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
    # name = band_name.name
    pprint.pprint(band_name)
    # band_name


    return render_template('musician_request.html', charts = band_charts, bands = Musician.get_all_band_w_musician(musician_id_dict), band_name = band_name)

    




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

