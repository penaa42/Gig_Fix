from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import musician_model

from flask import flash, session
import re

import pprint

db = 'gig_fix'

class Chart:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.chart_key = data['chart_key']
        self.time_signature = data['time_signature']
        self.tempo = data['tempo']
        self.band_id = data['band_id']
        self.record = None

    def __repr__(self) -> str:
        return f'Chart Repr ---------------> ID: {self.id} TITLE: {self.title} BAND ID: {self.band_id} RECORD: {self.record}'


########################################################
# VALIDATE CHART     chart_controller; route: /band/create_song; input request.form
    @staticmethod
    def validate_chart(form_data):

        is_valid = True

        if form_data['title'] == "":
            flash('Title is required, please enter Chart Title.')
            is_valid = False

        if form_data['chart_key'] == "" or len(form_data['chart_key']) < 1:
            flash('Key is required, please enter Chart Key.')
            is_valid = False

        if form_data['time_signature'] == "":
            flash('Time signature is required, please enter the Chart Time Signature.')
            is_valid = False

        if form_data['tempo'] == "" or form_data['tempo'] == 0:
            flash('Invalid tempo, please re-enter a Tempo.')
            is_valid = False

        return is_valid

########################################################
# CREATE CHART        chart_controller; route: /band/create_chart; input request.form; INSERT QUERY(input band_id)
    @classmethod
    def create_chart(cls, request_form_data):

        query = "INSERT INTO charts (title, chart_key, time_signature, tempo, band_id) VALUES (%(title)s, %(chart_key)s, %(time_signature)s, %(tempo)s, %(band_id)s);"
        db_response = connectToMySQL(db).query_db(query, request_form_data)

        print('-------------CREATE CHART DB RESPONSE-------------')
        pprint.pprint(db_response)

        return db_response


########################################################
# GET CHART WITH BAND     band_controller; input: chart_id; route: /band/requests
    @classmethod
    def get_charts_w_band(cls):
        query = "SELECT * FROM bands JOIN charts ON bands.id = charts.band_id"
        db_response = connectToMySQL(db).query_db(query)

        print('------------CHARTS WITH BAND DB RESPONSE-----------')
        pprint.pprint(db_response)

        charts = []

        for chart_and_band in db_response:
            if chart_and_band['band_id'] == session['band_id']:

                chart_data = {
                    'id' : chart_and_band['charts.id'],
                    'title' : chart_and_band['title'],
                    'chart_key' : chart_and_band['chart_key'],
                    'time_signature' : chart_and_band['time_signature'],
                    'tempo' : chart_and_band['tempo'],
                    'band_id' : chart_and_band['band_id']
                }

                new_chart = cls(chart_data)
                print('----------CHART DATA INTO NEW CHART CLASS----------')
                pprint.pprint(new_chart)

                charts.append(new_chart)

            print('---------CHECKING LIST OF SONG INSTANCES IN GET ALL----------')
            pprint.pprint(charts)

        return charts


########################################################
# SHOW CHART         chart_controller; route: /band/edit_chart/<int:chart_id>; input id_data dict; SELECT QUERY(chart_id input)
    @classmethod
    def show_chart(cls, show_data):
        query = "SELECT * FROM charts WHERE id = %(id)s;"
        db_response = connectToMySQL(db).query_db(query, show_data)

        print('----------SHOW CHART DB RESPONSE----------')
        pprint.pprint(db_response)

        for chart in db_response:
            new_chart = cls(chart)

        return new_chart


########################################################
# UPDATE CHART        chart_controller; route: /band/update/chart; input html request.form
    @classmethod
    def update_chart(cls, request_form_data):
        print('----UPDATE CHART FORM-------')
        pprint.pprint(request_form_data)

        query = "UPDATE charts SET title = %(title)s, chart_key = %(chart_key)s, time_signature = %(time_signature)s, tempo = %(tempo)s WHERE id = %(id)s;"
        db_response = connectToMySQL(db).query_db(query, request_form_data)

        return db_response


########################################################
# DELETE CHART        band_controller; route: /band/delete_chart/<int:chart_id>, input: chart_id
    @classmethod
    def delete_chart(cls, chart_id):
        query = "DELETE FROM charts WHERE id = %(id)s;"
        db_response = connectToMySQL(db).query_db(query, chart_id)

        return db_response


    @classmethod
    def profile_view_charts(cls, show_data):
        print('-----MUSICIAN TO CHART-----')
        pprint.pprint(show_data)

        query = "SELECT * FROM charts WHERE band_id = %(id)s"
        print(query)

        db_response = connectToMySQL(db).query_db(query, show_data)

        charts = []

        print('-------DB RESPONSE-------')
        pprint.pprint(db_response)

        for chart in db_response:
            new_chart = cls(chart)
            charts.append(new_chart)

        return charts
