from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/log')
def login_page():
    return render_template('log.html')

@app.route('/reg')
def register():
    return render_template('register.html')
































app.run(debug=True)