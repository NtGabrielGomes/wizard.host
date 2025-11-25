from flask import Flask, abort, redirect, url_for, render_template, request, jsonify, make_response, session

def page_not_found(e):
    return render_template('404.html'), 404