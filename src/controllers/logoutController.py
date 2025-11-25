from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session


def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', '', expires=0)  # Clear the token cookie
    return response
