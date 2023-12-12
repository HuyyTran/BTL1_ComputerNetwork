from flask import Blueprint, render_template, request, jsonify
from .server import file_server
from .client import client

views = Blueprint('views', __name__)

@views.route('/')
def home(): 
    return render_template('index.html')

@views.route('/server')
def server_view():
    return render_template('server.html')

@views.route('/client')
def client_view():
    return render_template('client.html')

@views.route('/start-server', methods=['POST'])
def handle_start_server():
    return file_server.start()

@views.route('/stop-server', methods=['POST'])
def handle_stop_server():
    return file_server.stop()

@views.route('/connect', methods=['POST'])
def handle_connect():
    server_ip = request.form.get('serverIp')
    server_port = request.form.get('serverPort')
    message = client.connect(server_ip, server_port)
    return jsonify(message), 200

@views.route('/disconnect', methods=['POST'])
def handle_disconnect():
    message = client.disconnect()
    return jsonify(message), 200