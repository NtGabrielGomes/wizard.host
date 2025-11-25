from src.Factory.database import db
from flask_sqlalchemy import SQLAlchemy
from .vpsView import Vps

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True) 
    wizard_name = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    cash = db.Column(db.Numeric(precision=10, scale=2), default=0.00)
    vps = db.relationship('Vps', backref='owner', lazy=True)  # Establishes a relationship with the Vps table

    # Cria uma string para o usuario
    def __repr__(self):
        return f"User {self.wizard_name}"


