import socket
import json

# Configuration
SERVER_IP = 'localhost'
SERVER_PORT = 5000

class P2PClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None
        self.connect_to_server()

    def connect_to_server(self):
        # Establish a connection to the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))

    def send_command_to_server(self, command):
        try:
            # Send command
            message = json.dumps(command).encode('utf-8')
            self.sock.sendall(message)

            # Look for the response
            response = self.sock.recv(4096).decode('utf-8')
            print(f"Received: {response}")

        except socket.error as e:
            print(f"Socket error: {e}")
            self.sock.close()
            self.connect_to_server()

    def close_connection(self):
        # Close the connection to the server
        self.sock.close()

    def publish(self, local_name, file_name):
        command = {
            "action": "publish",
            "lname": local_name,
            "fname": file_name
        }
        self.send_command_to_server(command)

    def fetch(self, file_name):
        command = {
            "action": "fetch",
            "fname": file_name
        }
        self.send_command_to_server(command)

    def discover(self, hostname):
        command = {
            "action": "discover",
            "hostname": hostname
        }
        self.send_command_to_server(command)

    def ping(self, hostname):
        command = {
            "action": "ping",
            "hostname": hostname
        }
        self.send_command_to_server(command)

# Example usage
if __name__ == '__main__':
    client = P2PClient(SERVER_IP, SERVER_PORT)
    print("Connected to the server. Enter commands: discover, ping, publish, fetch")
    
    try:
        while True:
            cmd_input = input("Enter command: ").strip().split()
            action = cmd_input[0].lower()

            if action == "discover" and len(cmd_input) == 2:
                client.discover(cmd_input[1])
            elif action == "ping" and len(cmd_input) == 2:
                client.ping(cmd_input[1])
            elif action == "publish" and len(cmd_input) == 3:
                client.publish(cmd_input[1], cmd_input[2])
            elif action == "fetch" and len(cmd_input) == 2:
                client.fetch(cmd_input[1])
            elif action == "exit":
                break
            else:
                print("Unknown command or incorrect parameters.")
    finally:
        print("Disconnecting from the server.")
        client.close_connection()
