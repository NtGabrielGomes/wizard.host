from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session
from src.models.userView import Users
from src.Factory.flaskInit import serializer

def pay():

    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))

    try:
        # Validate the token
        user_id = serializer.loads(token, salt='login', max_age=30*24*60*60)  # 30 days expiration
        user = Users.query.get(user_id)  # Fetch the user from the database
        if not user:
            return redirect(url_for('login'))
    except Exception:
        return redirect(url_for('login'))
    return render_template('pay.html', username=user.wizard_name)
