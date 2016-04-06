#!/bin/python
from flask import Flask, jsonify
from flask import render_template, redirect, url_for, request
import os
from werkzeug import secure_filename
import s3_sync
import dockers

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/test'
ALLOWED_EXTENSIONS = set(['txt', 'mp4', 'html', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/')
def index():
	return redirect(url_for('hello'))

@app.route('/login/	')
def login():
    return jsonify({'tasks': tasks})


# @app.route('/')
# def index():
#     return 'Hello world'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('hello'))


@app.route('/hello', methods=["POST", "GET"])
def hello(name=None):
    if request.method == 'POST':
    	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    return render_template('hello.html', name=s3_sync.s3_list_folder(request.args.get('folder')), test=request.args.get('folder'))

@app.route('/docker', methods=["POST", "GET"])
def docker(name=None):
    if request.method == 'POST':
        search = request.form['search']
        return render_template('docker.html', dockers=dockers.search_docker(dockers.docker_name_up(), search), test=request.args.get('folder'))
    else: 
        return render_template('docker.html', dockers=dockers.docker_name_up(), test=request.args.get('folder'))

#######################################
#######################################
import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
#######################################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')











