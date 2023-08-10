from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.musician_model import Musician
from flask_app.models.band_model import Band
from flask_app.models.song_model import Song
from flask_app.models.chart_model import Chart

import pprint

@app.route('/band/add_chart')
def add_chart_page():
    return render_template('add_chart.html')


@app.route('/band/create_chart', methods = ['POST'])
def create_chart():
    print('-----SESSION BAND ID-----')
    pprint.pprint(session['band_id'])

    print('-------CHECKING BEFORE CHART VALIDATE---------')
    pprint.pprint(request.form)

    if not Chart.validate_chart(request.form):
        print('FAILED CHART VALIDATION')
        flash('Failed to add the chart, please try again.')
        return redirect('/band/add_chart')

#   CREATE CHART
    chart_id = Chart.create_chart(request.form)
    session['chart_id'] = chart_id
    print('----NEW CHART ID----')
    print(session['chart_id'])

    return redirect('/band/requests')



@app.route('/band/edit_chart/<int:chart_id>')
def edit_chart_page(chart_id):
    # band_id = session['band_id']

    id_data = {
        'id' : chart_id
    }

    chart = Chart.show_chart(id_data)

    print('---------------SONG INFO PASSED TO HTML---------------')
    pprint.pprint(chart)


    return render_template('edit_song.html', chart = chart)

































