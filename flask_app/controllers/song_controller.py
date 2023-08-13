from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.musician_model import Musician
from flask_app.models.band_model import Band
from flask_app.models.song_model import Song

import pprint

@app.route('/profile/add_song')
def add_song_page():
# DASHBOARD: DISPLAY ALL SONGS WITH MUSICIAN
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')

    return render_template('add_song.html')


@app.route('/profile/create_song', methods = ['POST'])
def create_song():
    print('-----SESSION MUSICIAN ID-----')
    pprint.pprint(session['musician_id'])

    print('-------CHECKING BEFORE SONG VALIDATE---------')
    pprint.pprint(request.form)

    if not Song.validate_song(request.form):
        print('FAILED SONG VALIDATION')
        flash('Failed to add the song, please try again.')
        return redirect('/profile/add_song')

#   CREATE SONG
    song_id = Song.create_song(request.form)
    session['song_id'] = song_id

    return redirect('/profile')


@app.route('/profile/edit_song/<int:song_id>')
def edit_song_page(song_id):
    # DASHBOARD: DISPLAY ALL SONGS WITH MUSICIAN
    if not 'musician_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')

    id_data = {
        'id' : song_id
    }

    song = Song.show_song(id_data)

    print('---------------SONG INFO PASSED TO HTML---------------')
    pprint.pprint(song)

    return render_template('edit_song.html', song = song)


########################################################
# UPDATE SONG        html inputs: musician_id, request.form
@app.route('/profile/update/song', methods = ['POST'])
def update_song():
    print('------UPDATING SONG------')
    pprint.pprint(request.form)
    song_id = request.form['song_id']

    if not Song.validate_song_update(request.form):
        print("FAILED UPDATE SONG VALIDATION")
        return redirect(f'/profile/edit_song/{song_id}')

#   setting up dict for query from request.form
    show_data = {
        'id' : request.form['song_id'],
        'date' : request.form['date'],
        'city' : request.form['city'],
        'state' : request.form['state'],
        'link' : request.form['link']
    }

    print('-------------UPDATE SHOW DATA-------------')
    pprint.pprint(show_data)

#   call update method
    Song.update_song(show_data)

    return redirect('/profile')

