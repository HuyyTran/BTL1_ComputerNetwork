import socket
import threading
import json

# In-memory storage for client details and available files
clients = {}  # Stores client information
files = {}    # Stores which client has which files

def handle_discover(conn):
    # Return a list of all hostnames (client addresses)
    hostnames = list(clients.keys())
    conn.send(json.dumps(hostnames).encode('utf-8'))

def handle_ping(conn, hostname):
    # Check if the specified hostname is in the client list
    response = "active" if hostname in clients else "inactive"
    conn.send(response.encode('utf-8'))

def handle_client(conn, addr):
    # Handle client commands
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = json.loads(data.decode('utf-8'))
            action = command.get('action', '')
            if action == 'discover':
                handle_discover(conn)
            elif action == 'ping':
                hostname = command.get('hostname', '')
                handle_ping(conn, hostname)
            else:
                conn.send(b'Invalid command')
    except Exception as e:
        print(f"An error occurred with client {addr}: {e}")
    finally:
        conn.close()
        clients.pop(addr, None)  # Remove client from in-memory storage

def start_server(host='0.0.0.0', port=5000):
    # Start server and listen for connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server is listening on {host}:{port}")
    while True:
        conn, addr = server.accept()
        print(f"Accepted connection from {addr}")
        clients[addr] = {'conn': conn, 'files': []}  # Initialize client data
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
