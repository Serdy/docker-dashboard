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
	return redirect(url_for('docker'))

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
    if 'search' in request.args:
        search = request.args['search']
        return render_template('docker.html', dockers=dockers.search_docker(dockers.docker_name_up(), search))
    elif 'intro' in request.args:
        docker_host = request.args['docker_host']
        docker_id = request.args['docker_id']
        return render_template('docker_intro.html', docker=dockers.docker_intro(docker_host, docker_id))
    elif 'docker_log' in request.args:
        docker_host = request.args['docker_host']
        docker_id = request.args['docker_id']
        return render_template('docker_logs.html', dockers=dockers.docker_logs(docker_host, docker_id), docker_id=docker_id, docker_host=docker_host)
    elif 'docker_top' in request.args:
        docker_host = request.args['docker_host']
        docker_id = request.args['docker_id']
        return render_template('docker_top.html', dockers=dockers.docker_top(docker_host, docker_id), docker_id=docker_id, docker_host=docker_host)
    else: 
        return render_template('docker.html', dockers=dockers.docker_name_up(), test=request.args.get('folder'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')











