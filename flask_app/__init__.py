from flask import Flask
app = Flask(__name__)
app.secret_key = 'Save the Gig, save the world!'


upload_folder = '/flask_app/static/assests/img/profile/'
app.config['upload_folder'] = upload_folder