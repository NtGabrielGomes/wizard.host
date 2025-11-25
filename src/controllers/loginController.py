from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.userView import Users
from src.Factory.flaskInit import serializer

def login():

    if request.method == "POST":
        
        nome = request.form.get('username')
        senha = request.form.get('password')
        
        if not nome or not senha:
            return render_template('login.html', resu="Preencha todos os campos"), 400

        user_db = Users.query.filter_by(email=nome).first()
        if user_db and check_password_hash(user_db.password, senha):
            # Gera o token com base no nome do usuário
            token = serializer.dumps(user_db.id, salt='login')  
                      
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie(
                'token',
                value=token,
                max_age=30*24*60*60,   # 30 dias
                secure=True,
                httponly=True,
                samesite='Strict'   
            )
            return response
        else:
            return render_template('login.html', resu="Senha incorreta"), 401
    else:
        return render_template('login.html'), 403  