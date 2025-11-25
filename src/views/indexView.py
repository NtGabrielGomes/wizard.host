from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session

def index():
    return render_template('index.html')