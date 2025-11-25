from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session

def login_page():
    return render_template('login.html')