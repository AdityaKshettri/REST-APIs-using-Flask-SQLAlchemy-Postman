from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Aditya Kshettri/Documents/FlaskRestApi/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
