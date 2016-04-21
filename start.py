#!/bin/python
from flask import Flask, jsonify
from flask import render_template, redirect, url_for, request
import os
from werkzeug import secure_filename
import dockers

app = Flask(__name__)


@app.route('/')
def index():
	return redirect(url_for('docker'))


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
    app.run(host='0.0.0.0')











