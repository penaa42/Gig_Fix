from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import musician_model
from flask import flash
import re

import pprint

db = 'gig_fix'

class Song:
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.city = data['city']
        self.state = data['state']
        self.link = data['link']
        self.musician_id = data['musician_id']
        self.performance = None

    def __repr__(self) -> str:
        return f'Song Repr ---------------> ID: {self.id} CITY: {self.city} MUSICIAN ID: {self.musician_id} PERFORMANCE: {self.performance}'


########################################################
# VALIDATE SONG     song_controller; route: /profile/create_song; input request.form
    @staticmethod
    def validate_song(form_data):

        is_valid = True

        if form_data['date'] == "":
            flash('Date is required, please enter Performance Date.')
            is_valid = False

        if form_data['city'] == "":
            flash('City is required, please enter City.')
            is_valid = False

        if len(form_data['state']) != 2:
            flash('State is required, please enter State abbreviation.')
            is_valid = False

        if form_data['link'] == "":
            flash('Link is required, please enter embeded link to the performance.')
            is_valid = False

        elif 'http' not in form_data['link']:
            flash('Invalid link. Please double check performance link.')
            is_valid = False

        return is_valid


########################################################
# CREATE SONG        song_controller; route: /profile/create_song; input request.form; INSERT QUERY(input)
    @classmethod
    def create_song(cls, request_form_data):
        query = "INSERT INTO songs (date, city, state, link, musician_id) VALUES (%(date)s, %(city)s, %(state)s, %(link)s, %(musician_id)s);"
        db_response = connectToMySQL(db).query_db(query, request_form_data)

        print('-------------CREATE SONG DB RESPONSE-------------')
        pprint.pprint(db_response)

        return db_response


########################################################
# GET SONG WITH MUSICIAN     musician_controller; input: song_id; route: /profile
    @classmethod
    def get_songs_w_musician(cls):
        query = "SELECT * FROM musicians JOIN songs ON musicians.id = songs.musician_id"
        db_response = connectToMySQL(db).query_db(query)

        print('------------SONGS WITH MUSICIAN DB RESPONSE-----------')
        pprint.pprint(db_response)

        songs = []

        for song_and_musician in db_response:
            song_data = {
                'id' : song_and_musician['songs.id'],
                'date' : song_and_musician['date'],
                'city' : song_and_musician['songs.city'],
                'state' : song_and_musician['songs.state'],
                'link' : song_and_musician['link'],
                'musician_id' : song_and_musician['musician_id']
            }

            new_song = cls(song_data)
            print('----------SONG DATA INTO NEW SONG CLASS----------')
            pprint.pprint(new_song)

            new_song.performance = musician_model.Musician(song_and_musician)
            print('------------CHECKING PERFORMANCE ATTRIBUTE CLASS ASSOCIATION------------')
            pprint.pprint(new_song.performance)

            print('-----LOOK AT MUSICIAN SONGS ATT------')
            new_song.performance.songs.append(new_song.link)
            pprint.pprint(new_song.performance.songs)

            songs.append(new_song)

        print('---------CHECKING LIST OF SONG INSTANCES IN GET ALL----------')
        pprint.pprint(songs)

        return songs


########################################################
# SHOW SONG         song_controller; route: /profile/edit_song/<int:song_id>; input id_data dict; SELECT QUERY(song_id input)
    @classmethod
    def show_song(cls, show_data):
        query = "SELECT * FROM songs WHERE id = %(id)s;"
        db_response = connectToMySQL(db).query_db(query, show_data)

        print('----------SHOW SONG DB RESPONSE----------')
        pprint.pprint(db_response)

        for song in db_response:
            new_song = cls(song)

        return new_song


# VALIDATE SONG     song_controller; route: /profile/create_song; input request.form
    @staticmethod
    def validate_song_update(form_data):
        is_valid = True

        if form_data['date'] == "":
            flash('Date is required, please enter Performance Date.')
            is_valid = False

        if form_data['city'] == "":
            flash('City is required, please enter City.')
            is_valid = False

        if len(form_data['state']) != 2:
            flash('State is required, please enter State abbreviation.')
            is_valid = False

        if form_data['link'] == "":
            flash('Link is required, please enter embeded link to the performance.')
            is_valid = False

        elif 'http' not in form_data['link']:
            flash('Invalid link. Please double check the embeded link.')
            is_valid = False

        return is_valid


########################################################
# UPDATE SONG        song_controller; route: /profile/update/song; input html request.form
    @classmethod
    def update_song(cls, request_form_data):
        print('----UPDATE SONG FORM-------')
        pprint.pprint(request_form_data)

        query = "UPDATE songs SET date = %(date)s, city = %(city)s, state = %(state)s, link = %(link)s WHERE id = %(id)s;"
        db_response = connectToMySQL(db).query_db(query, request_form_data)

        return db_response


########################################################
# DELETE SONG        musician_controller; route: /profile/delete_song/<int:song_id>, input: song_id
    @classmethod
    def delete_song(cls, song_id):
        query = "DELETE FROM songs WHERE id = %(id)s;"
        db_response = connectToMySQL(db).query_db(query, song_id)

        return db_response
