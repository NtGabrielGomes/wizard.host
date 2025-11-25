from src.Factory.database import db

from flask_sqlalchemy import SQLAlchemy

class Vps(db.Model):
    vps_id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to Users table
    vps_name = db.Column(db.String(100), nullable=False)
    vps_expiration = db.Column(db.DateTime, nullable=False)