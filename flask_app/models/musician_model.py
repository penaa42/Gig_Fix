from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

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
        self.songs = []
        

    def __repr__(self) -> str:
        return f'Musician Repr ---------------> ID: {self.id} FIRST NAME: {self.first_name}: Recipes {self.songs}'


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

        if len(form_data['experience']) < 0:
            flash('Experience cannot be less than 0!', 'category1')
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


# VALIDATE LOGIN         musician_controller; route: /musician/login; html index request.form; SELECT QUERY(email input)
    @classmethod
    def find_musician_email(cls, email_dict):
        query = "SELECT * from musicians WHERE email = %(email)s"
        db_response = connectToMySQL(db).query_db(query, email_dict)

        # should get back a list(one) of dict---> email does exist
        # should get back an empty list if email doesn't exist
        print('----------FIND MUSICIAN EMAIL DB RESPONSE------------',db_response)

        if len(db_response) < 1:
            return False
        # creating an instance from the query result (db_response)
        return cls(db_response[0])



########################################################
# CREATE MUSICIAN         musician_controller; route: /musician/register; INSERT QUERY(request.form input)
    @classmethod
    def create_musician(cls, request_form_data):
        query = "INSERT INTO musicians (first_name, last_name, genre, city, state, experience, description, instrument, email, password) VALUES (%(first_name)s, %(last_name)s, %(genre)s, %(city)s, %(state)s, %(experience)s, %(description)s, %(instrument)s, %(email)s, %(password)s);"
        db_response = connectToMySQL(db).query_db(query, request_form_data)

        print('-----------CREATE MUSICIAN DB RESPONSE-----------', db_response)
        return db_response


########################################################
# GET ALL MUSICIANS     band_controller; route: /dashboard; SELECT query(no input)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM musicians;"
        db_response = connectToMySQL(db).query_db(query)

        print('--------------GET ALL MUSICIANS DB RESPONSE------------', db_response)
#       list of car class instances for html loop
        musicians= []

        # for musician in db_response:
        #     new_musician = cls(musician)
        #     musicians.append(new_musician)

        # for musician in db_response:
#           reconstruct dict data to grab correct id in db_response for Car class (class association setup)
#             car_data = {
#                 'id' : car_and_user['cars.id'],
#                 'price' : car_and_user['price'],
#                 'model' : car_and_user['model'],
#                 'make' : car_and_user['make'],
#                 'year' : car_and_user['year'],
#                 'description' : car_and_user['description'],
#                 'created_at' : car_and_user['created_at'],
#                 'updated_at' : car_and_user['updated_at'],
#                 'user_id' : car_and_user['user_id']
# #                leave out seller class association
#             }

#           car dict turned into car class instance (no class association yet)
#             new_ = cls(car_data)
#             # print('----------CAR DATA INTO NEW CAR CLASS----------')
#             pprint.pprint(new_car)

# #           bringing in class association (user class placed in car attribute 'self.seller')
#             new_car.seller = user_model.User(car_and_user)
#             # print('------------CHECKING SELLER ATTRIBUTE CLASS ASSOCIATION------------')
#             pprint.pprint(new_car.seller)

# #           adding new_car class instance to cars list
#             cars.append(new_car)

#         # print('---------CHECKING LIST OF CAR INSTANCES IN GET ALL----------')
#         pprint.pprint(cars)

        return musicians






















    # @classmethod
    # def rename(cls):
    #     query = "SELECT * FROM users;"
    #     results = connectToMySQL(db).query_db(query)
    #     #Nice little head start
    #     #Rest of code here
    #     print(results)
    #     return "Something here"