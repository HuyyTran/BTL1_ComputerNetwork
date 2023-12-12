from flask import Flask, jsonify, request, Blueprint
import threading
import socket

# app = Flask(__name__)
server = Blueprint('server_real', __name__)

# Global variables to hold server state
server_socket = None
server_thread = None
clients_lock = threading.Lock()
clients = {}

def start_server(host, port):
    global server_socket
    global server_thread
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    server_thread = threading.Thread(target=listen_to_clients, args=(server_socket,), daemon=True)

    server_thread.start()
    return True

def stop_server():
    global server_socket
    if server_socket:
        server_socket.close()
    return True

def listen_to_clients(sock):
    while True:
        client_conn, client_addr = sock.accept()
        with clients_lock:
            clients[client_addr] = client_conn
        # Here you would start a new thread to handle the client connection

@server.route('/server/start', methods=['POST'])
def api_start_server():
    data = request.json
    host = data['host']
    port = data['port']
    print(host,port)
    if start_server(host, port):
        return jsonify({'status': 'success', 'message': 'Server started.'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to start server.'}), 500

@server.route('/server/stop', methods=['POST'])
def api_stop_server():
    if stop_server():
        return jsonify({'status': 'success', 'message': 'Server stopped.'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to stop server.'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
