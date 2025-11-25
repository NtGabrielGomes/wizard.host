from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session
from src.Factory.flaskInit import serializer
from src.models.userView import Users

def validate_token():
    token = request.cookies.get('token')
    if not token:
        return None, "Usuário não autenticado."

    try:
        # Valida o token e obtém o ID do usuário
        user_id = serializer.loads(token, salt='login', max_age=30*24*60*60)
        user = Users.query.get(user_id)
        if not user:
            return False
        return True
    except Exception:
        return False