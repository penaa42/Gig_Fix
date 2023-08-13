from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import band_model
from flask import flash

from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt

import uuid as uuid
import os
import re
import pprint

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db = 'gig_fix'

class Musician:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.genre = data['genre']
        self.city = data['city']
        self.state = data['state']
        self.experience = data['experience']
        self.description = data['description']
        self.instrument = data['instrument']
        self.availability = data['availability']
        #db is saving image as a string
        self.profile_pic = data['profile_pic']
        self.songs = []


    def __repr__(self) -> str:
        return f'Musician Repr ---------------> ID: {self.id} FIRST NAME: {self.first_name} SONGS: {self.songs}'

###############################################################################################3
# 8) validate musician
#   musician_controller; route: /musician/register
    @staticmethod
    def validate_musician(form_data):
        is_valid = True

        if len(form_data['first_name']) < 2:
            flash('First name must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['last_name']) < 2:
            flash('Last name must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['genre']) < 2:
            flash('Genre must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['city']) < 2:
            flash('City must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['state']) != 2:
            flash('Please use state abbreviation!', 'category1')
            is_valid = False

        if form_data['experience'] == "":
            flash('Experience was left empty! Please add your experience', 'category1')
            is_valid = False

        if len(form_data['availability']) < 3:
            flash('Availability cannot be less than 3 characters!', 'category1')
            is_valid = False

        if len(form_data['password']) < 8:
            flash('Password must be at least 8 characters long!', 'category1')
            is_valid = False

        if len(form_data['instrument']) < 4:
            flash('Instrument cannot be less than 4 characters!', 'category1')
            is_valid = False

        if len(form_data['description']) == 0:
            flash('Please add your description', 'category1')
            is_valid = False

        if not EMAIL_REGEX.match(form_data['email']): 
            flash('Invalid email/password!', 'category1')
            is_valid = False

        if form_data['password'] != form_data['confirm_password']:
            flash('Invalid email/password!', 'category1')
            is_valid = False

        return is_valid


# VALIDATE LOGIN         musician_controller; route: /musician/login; html index request.form; SELECT QUERY(email input)
    @classmethod
    def find_musician_email(cls, email_dict):
        query = "SELECT * from musicians WHERE email = %(email)s"
        db_response = connectToMySQL(db).query_db(query, email_dict)

        # should get back a list(one) of dict---> email does exist
        # should get back an empty list if email doesn't exist
        print('----------FIND MUSICIAN EMAIL DB RESPONSE------------')
        pprint.pprint(db_response)

        if len(db_response) < 1:
            return False
        # creating an instance from the query result (db_response)
        return cls(db_response[0])

########################################################
# CREATE MUSICIAN         musician_controller; route: /musician/register; INSERT QUERY(request.form input)
    @classmethod
    def create_musician(cls, request_form_data):
        query = "INSERT INTO musicians (first_name, last_name, genre, city, state, experience, description, instrument, availability, email, password) VALUES (%(first_name)s, %(last_name)s, %(genre)s, %(city)s, %(state)s, %(experience)s, %(description)s, %(instrument)s, %(availability)s, %(email)s, %(password)s);"
        db_response = connectToMySQL(db).query_db(query, request_form_data)

        print('-----------CREATE MUSICIAN DB RESPONSE-----------')
        pprint.pprint(db_response)

        return db_response

########################################################
# GET ALL MUSICIANS     band_controller; route: /dashboard; SELECT query(no input)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM musicians;"
        db_response = connectToMySQL(db).query_db(query)

        print('--------------GET ALL MUSICIANS DB RESPONSE------------')
        pprint.pprint(db_response)
#       list of car class instances for html loop
        musicians= []

        for musician in db_response:
            new_musician = cls(musician)
            musicians.append(new_musician)

        print('-----CHECKING GET ALL MUSICIANS LIST-----')
        pprint.pprint(musicians)

        return musicians

########################################################
# SHOW MUSICIAN         musician_controller; route: /profile; input id_data dict; SELECT QUERY(musician_id input)
    @classmethod
    def show_musician(cls, show_data):
        query = "SELECT * FROM musicians WHERE id = %(id)s;"
        db_response = connectToMySQL(db).query_db(query, show_data)

        print('----------SHOW MUSICIAN DB RESPONSE----------')
        pprint.pprint(db_response)

        musician_first_name = db_response[0]['first_name']
        print('----------SHOW USER FIRST NAME----------')
        pprint.pprint(musician_first_name)

        for musician in db_response:
            new_musician = cls(musician)

        return new_musician

    @staticmethod
    def validate_musician_update(form_data):
        is_valid = True

        if len(form_data['first_name']) < 2:
            flash('First name must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['last_name']) < 2:
            flash('Last name must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['genre']) < 2:
            flash('Genre must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['city']) < 2:
            flash('City must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['state']) != 2:
            flash('Please use state abbreviation!', 'category1')
            is_valid = False

        if form_data['experience'] == "":
            flash('Experience was left empty! Please add your experience!', 'category1')
            is_valid = False

        if len(form_data['availability']) < 3:
            flash('Availability cannot be less than 3 characters!', 'category1')
            is_valid = False

        if len(form_data['instrument']) < 4:
            flash('Instrument cannot be less than 4 characters!', 'category1')
            is_valid = False

        if len(form_data['description']) == 0:
            flash('Please add your description', 'category1')
            is_valid = False

        return is_valid

########################################################
# UPDATE MUSICIAN        musician_controller; route: /profile/update; input html request.form
    @classmethod
    def update_profile(cls, request_form_data):
        print('-----------UPDATE DATA INTO CLASSMETHOD-----------')
        pprint.pprint(request_form_data)
        query = "UPDATE musicians SET first_name = %(first_name)s, last_name = %(last_name)s, genre = %(genre)s, city = %(city)s, state = %(state)s, experience = %(experience)s, instrument = %(instrument)s, availability = %(availability)s, description = %(description)s WHERE id = %(id)s;"
        db_response = connectToMySQL(db).query_db(query, request_form_data)

        return db_response

########################################################
# GET MUSICIAN WITH BANDS     musician_controller; input: musician_id; route: /profile/requests/<int:musician_id>
    @classmethod
    def get_all_band_w_musician(cls, musician_id_dict):

        print('-----JOIN QUERY DICT-----')
        pprint.pprint(musician_id_dict)

        query = "SELECT * FROM bands JOIN bands_musicians ON bands.id = bands_musicians.band_id JOIN musicians ON musicians.id = bands_musicians.musician_id;"

        db_response = connectToMySQL(db).query_db(query)

        print('-------MUSICIAN WITH BANDS DB RESPONSE--------')
        pprint.pprint(db_response)

        bands = []

        for band_and_musician in db_response:
            if band_and_musician['musician_id'] == musician_id_dict['id']:
                band_data = {
                    'id' : band_and_musician['band_id'],
                    'name' : band_and_musician['name'],
                    'city' : band_and_musician['city'],
                    'state' : band_and_musician['state'],
                    'email' : band_and_musician['email'],
                    'password' : band_and_musician['password'],
                    'created_at' : band_and_musician['created_at'],
                    'updated_at' : band_and_musician['updated_at']
                }

                new_band = band_model.Band(band_data)
                print('----------BAND DATA INTO NEW BAND CLASS----------')
                pprint.pprint(new_band)

                bands.append(new_band)

        print('---------CHECKING LIST OF REQUESTS INSTANCES IN GET ALL----------')
        pprint.pprint(bands)

        return bands

########################################################
# DELETE BAND FROM MUSICIAN REQUESTS     musician_controller; input: band_id, musician_id; route: /profile/requests/decline/<int:band_id>/<int:musician_id>
    @classmethod
    def delete_band_w_musician(cls, delete_data):

        print('-----DELETE DATA FROM MUSICIAN DELETE BAND DICT -----')
        pprint.pprint(delete_data)

        query = '''DELETE FROM bands_musicians 

        WHERE musician_id = %(musician_id)s 

        AND band_id = %(band_id)s'''

        pprint.pprint(query)

        db_response = connectToMySQL(db).query_db(query, delete_data)
        print('-----DLELET DATA DB RESPONSE-----')
        pprint.pprint(db_response)

        return

########################################################
# PROFILE PIC     musician_controller; input: request.form; route: /profile/upload
    @classmethod
    def add_image(cls, pic_dict):

        print('------PIC CLASSMETHOD REQUEST FORM------')
        pprint.pprint(pic_dict)

        query = '''UPDATE musicians SET 

        profile_pic = %(profile_pic)s 

        WHERE id = %(id)s'''

        print('-----PIC QUERY------')
        pprint.pprint(query)

        db_response = connectToMySQL(db).query_db(query, pic_dict)
        print('------PIC DB RESPONSE-----')
        pprint.pprint(db_response)

        return

    @staticmethod
    def validate_profile_img(form_data):
        is_valid = True

        print('-----MUSICIAN MODEL FORM DATA----')
        print(len(form_data))

        profile_pic = form_data['profile_pic']
        print('------MUSICIAN MODEL PROFILE_PIC----')
        print(profile_pic)

        pic_filename = secure_filename(profile_pic.filename)
        print('------MUSICIAN MODEL PIC_FILENAME-----')
        print(pic_filename)

        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

        if len(pic_filename) < 1:
            flash('File was not selected, please select a photo!')
            is_valid = False

        elif pic_filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            flash('Incorrect file type selected, please select png, jpg, jpeg, or gif file')
            is_valid = False

        return is_valid
