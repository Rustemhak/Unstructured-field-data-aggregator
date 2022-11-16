from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Started<h1>'


@app.route('/badrequest400')
def bad_request():
    return abort(400)


