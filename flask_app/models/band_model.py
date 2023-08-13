from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import musician_model
from flask import flash, session
import re

import pprint

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db = 'gig_fix'

class Band:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.city = data['city']
        self.state = data['state']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.charts = []

    def __repr__(self) -> str:
        return f'Band Repr ---------------> ID: {self.id} NAME: {self.name} CHARTS: {self.charts}'

###############################################################################################3
# VALIDATE BAND REGISTER       band_controller; route: /band/register
    @staticmethod
    def validate_band(form_data):
        is_valid = True

        if len(form_data['name']) < 2:
            flash('Band name must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['city']) < 2:
            flash('City must be at least 2 characters long!', 'category1')
            is_valid = False

        if len(form_data['state']) != 2:
            flash('Please use state abbreviation!', 'category1')
            is_valid = False

        if len(form_data['password']) < 8:
            flash('Password must be at least 8 characters long!', 'category1')
            is_valid = False

        if not EMAIL_REGEX.match(form_data['email']): 
            flash('Invalid email/password!', 'category1')
            is_valid = False

        if form_data['password'] != form_data['confirm_password']:
            flash('Invalid email/password!', 'category1')
            is_valid = False

        return is_valid


# VALIDATE LOGIN         band_controller; route: /band/login; html index request.form; SELECT QUERY(email input)
    @classmethod
    def find_band_email(cls, email_dict):
        query = "SELECT * from bands WHERE email = %(email)s"
        db_response = connectToMySQL(db).query_db(query, email_dict)

        # should get back a list(one) of dict---> email does exist
        # should get back an empty list if email doesn't exist
        print('----------FIND BAND EMAIL DB RESPONSE------------')
        pprint.pprint(db_response)

        if len(db_response) < 1:
            return False
        # creating an instance from the query result (db_response)
        return cls(db_response[0])


########################################################
# CREATE BAND         band_controller; route: /band/register; INSERT QUERY(request.form input)
    @classmethod
    def create_band(cls, request_form_data):
        query = "INSERT INTO bands (name, city, state, email, password) VALUES (%(name)s, %(city)s, %(state)s, %(email)s, %(password)s);"
        db_response = connectToMySQL(db).query_db(query, request_form_data)

        print('-----------CREATE BAND DB RESPONSE-----------')
        pprint.pprint(db_response)

        return db_response

# CREATE GIG REQUEST        band_controller; route /band/gig/request; INSERT QUERY(request.form input)
    @classmethod
    def create_gig_request(cls, request_form_data):

        print('----GIG REQUEST FORM DATA------')
        pprint.pprint(request_form_data)

        query = "INSERT INTO bands_musicians (band_id, musician_id) VALUES (%(band_id)s, %(musician_id)s);"
        db_response = connectToMySQL(db).query_db(query, request_form_data)

        print('------GIG REQUEST DB RESPONSE-----')
        pprint.pprint(db_response)

        return


########################################################
# GET BANDS WITH MUSICIANS     band_controller; input: band_id; route: /band/requests/<int:band_id>?
    @classmethod
    def get_all_musician_w_band(cls, band_id_dict):

        print('-----JOIN QUERY DICT-----')
        pprint.pprint(band_id_dict)

        query = "SELECT * FROM musicians JOIN bands_musicians ON musicians.id = bands_musicians.musician_id JOIN bands ON bands.id = bands_musicians.band_id"
        print(query)

        db_response = connectToMySQL(db).query_db(query)

        print('-------BAND WITH MUSICIAN DB RESPONSE--------')
        pprint.pprint(db_response)

        musicians = []

        for musician_and_band in db_response:
            if musician_and_band['band_id'] == band_id_dict['id']:
                musician_data = {
                    'id' : musician_and_band['musician_id'],
                    'first_name' : musician_and_band['first_name'],
                    'last_name' : musician_and_band['last_name'],
                    'email' : musician_and_band['email'],
                    'password' : musician_and_band['password'],
                    'created_at' : musician_and_band['created_at'],
                    'updated_at' : musician_and_band['updated_at'],
                    'genre' : musician_and_band['genre'],
                    'city' : musician_and_band['city'],
                    'state' : musician_and_band['state'],
                    'experience' : musician_and_band['experience'],
                    'description' : musician_and_band['description'],
                    'instrument' : musician_and_band['instrument'],
                    'availability' : musician_and_band['availability'],
                    'profile_pic' : musician_and_band['profile_pic']
                }

                new_musician = musician_model.Musician(musician_data)
                print('----------BAND DATA INTO NEW BAND CLASS----------')
                pprint.pprint(new_musician)

                musicians.append(new_musician)

        print('---------CHECKING LIST OF REQUESTS INSTANCES IN GET ALL----------')
        pprint.pprint(musicians)

        return musicians


########################################################
# SHOW BAND         band_controller; route: /band/requests/; input band_id_data dict; SELECT QUERY(band_id input)
    @classmethod
    def show_band(cls, show_data):
        query = "SELECT * FROM bands WHERE id = %(id)s;"
        db_response = connectToMySQL(db).query_db(query, show_data)

        print('----------SHOW BAND DB RESPONSE----------')
        pprint.pprint(db_response)

        band_name = db_response[0]['name']
        print('----------SHOW USER FIRST NAME----------')
        pprint.pprint(band_name)

        for band in db_response:
            new_band = cls(band)

        return new_band


########################################################
# DELETE MUSICIANS FROM BAND REQUESTS     band_controller; input: band_id; route: /band/requests/<int:band_id>?
    @classmethod
    def delete_musician_w_band(cls, delete_data):
        print('-----DELETE DATA DICT MUSICIAN_ID-----')
        pprint.pprint(delete_data)

    #  grab id where band_id and musician_id are the same
        print('-----PRINTING NEW QUERY-----')

        query = '''DELETE FROM bands_musicians 

        WHERE musician_id = %(musician_id)s 

        AND band_id = %(band_id)s'''

        pprint.pprint(query)

        db_response = connectToMySQL(db).query_db(query, delete_data)
        print('-----JOINED DICT DB RESPONSE-----')
        pprint.pprint(db_response)

        return

