from flask import Flask
app = Flask(__name__)
app.secret_key = 'Save the Gig, save the world!'


UPLOAD_FOLDER = "/static/assests/img/profile"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER