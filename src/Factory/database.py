from flask_sqlalchemy import SQLAlchemy
from .flaskInit import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()