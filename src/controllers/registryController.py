from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session
import magic_name
from src.models.userView import Users
from src.Factory.database import db
import re
from werkzeug.security import generate_password_hash, check_password_hash


def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        # Validações
        if not email or not password or not confirm_password:
            return render_template('register.html', resu="⚠️ Preencha todos os campos."), 400

        if password != confirm_password:
            return render_template('register.html', resu="❌ As senhas não coincidem."), 400

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return render_template('register.html', resu="📧 Email inválido."), 400

        if len(password) < 5:
            return render_template('register.html', resu="🔒 Sua chave secreta é curta :( "), 400
        
        if not any(char.isupper() for char in password) or \
           not any(char.isdigit() for char in password) or \
           not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
            return render_template('register.html', resu="🧙 Exemplo de senha: !M3d13v4lW0rd@"), 400

        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', resu="📛 Email já registrado."), 400

        # Colocando no banco de dados 
        # hash da senha 
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=12)
        wizard_name = magic_name.create_a_wizard()
        
        # query para criar um usuario
        new_user = Users(
            email=email, 
            password=hashed_password, 
            wizard_name=wizard_name
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template('register.html', resu=f"⚠️ Erro ao registrar o usuário. {e}"), 500           
        return render_template('register.html', resu="✅ Usuário registrado com sucesso! ✨!"), 200
    else:
        return redirect(url_for('registro'))