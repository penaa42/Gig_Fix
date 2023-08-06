from flask_app import app 
from flask_app.controllers import musician_controller
from flask_app.controllers import band_controller
from flask_app.controllers import song_controller
from flask_app.controllers import chart_controller

if __name__=='__main__':
    app.run(debug=True, port=5000)