from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session

def registro():
    return render_template('register.html')