from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.musician_model import Musician
from flask_app.models.band_model import Band
from flask_app.models.song_model import Song
from flask_app.models.chart_model import Chart

import pprint

@app.route('/band/add_chart')
def add_chart_page():
    # DASHBOARD: DISPLAY ALL SONGS WITH MUSICIAN
    # if not 'musician_id' in session:
    #     print('FAILED MUSICIAN SESSION VALIDATION')
    #     return redirect('/')
    if not 'band_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')
    
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
    # DASHBOARD: DISPLAY ALL SONGS WITH MUSICIAN
    # if not 'musician_id' in session:
    #     print('FAILED MUSICIAN SESSION VALIDATION')
    #     return redirect('/')
    if not 'band_id' in session:
        print('FAILED MUSICIAN SESSION VALIDATION')
        return redirect('/')
    # band_id = session['band_id']

    id_data = {
        'id' : chart_id
    }

    chart = Chart.show_chart(id_data)

    print('---------------CHART INFO PASSED TO HTML---------------')
    pprint.pprint(chart)


    return render_template('edit_chart.html', chart = chart)




########################################################
# UPDATE CHART        html inputs: band_id, request.form
@app.route('/band/update/chart', methods = ['POST'])
def update_chart():
    print('------UPDATING CHART------')
    pprint.pprint(request.form)
    # car_id = session['car_id']

    # if not Car.validate_car(request.form):
    #     print("FAILED UPDATE CAR VALIDATION")
    #     return redirect(f'/edit_page/{car_id}')

#   setting up dict for query from request.form
    show_data = {
        'id' : request.form['chart_id'],
        'title' : request.form['title'],
        'chart_key' : request.form['chart_key'],
        'time_signature' : request.form['time_signature'],
        'tempo' : request.form['tempo']
    }

    print('-------------UPDATE SHOW DATA-------------')
    pprint.pprint(show_data)

# #   call update method
    Chart.update_chart(show_data)

    return redirect('/band/requests/')




























