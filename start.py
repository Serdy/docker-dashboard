#!/bin/python
from flask import Flask
from flask import render_template, redirect, url_for, request
# import os
# from werkzeug import secure_filename
import dockers
import sql
from flask import g
import sqlite3


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



@app.route('/setting', methods=["POST", "GET"])
def emails():
    if request.method == 'POST':
        for get_request in request.form:
            if 'add_host' == get_request :
                host_ip = request.form['host_ip']
                domain_name = request.form['domain_name']
                datacenter = request.form['datacenter']
                sql.add_host(host_ip, domain_name, datacenter)
                return render_template('setting.html', hosts=sql.hosts())
            elif 'del_host'  == get_request:
                host_id = request.form['host_id']
                sql.del_host(host_id)
                return render_template('setting.html', hosts=sql.hosts())
    else:
        return render_template('setting.html', hosts=sql.hosts())


@app.before_request
def before_request():
    try:
        g.db = sqlite3.connect("flask.db")        
    except Exception:
        pass
    
   
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')











