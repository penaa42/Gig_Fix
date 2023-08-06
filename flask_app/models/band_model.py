from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

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
        return f'Band Repr ---------------> ID: {self.id} NAME: {self.name}: Charts {self.charts}'

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
        print('----------FIND BAND EMAIL DB RESPONSE------------',db_response)

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

        print('-----------CREATE BAND DB RESPONSE-----------', db_response)
        return db_response
    