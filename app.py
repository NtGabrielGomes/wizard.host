from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session
from src.Factory.database import db
from src.Factory.flaskInit  import app
from src.routes.routes import init_routes


init_routes(app)
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()  # RETIRAR EM PRODUÇÂO 
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True, host="127.0.0.1", port=80)