import cmd
import threading
import socket
import json

class ServerCmd(cmd.Cmd):
    intro = 'Welcome to the P2P server shell. Type help or ? to list commands.\n'
    prompt = '(server) '

    def __init__(self, host, port):
        super().__init__()
        self.server_host = host
        self.server_port = port
        self.server_socket = None
        self.clients = {}  # Dictionary to store client address and socket object
        self.clients_lock = threading.Lock()  # A lock to protect shared resources

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_host, self.server_port))
        self.server_socket.listen()
        print(f"Server listening on {self.server_host}:{self.server_port}")
        threading.Thread(target=self.listen_to_clients, daemon=True).start()

    def listen_to_clients(self):
        while True:
            client_conn, client_addr = self.server_socket.accept()
            with self.clients_lock:
                self.clients[client_addr] = client_conn
            print(f"New client connected: {client_addr}")
            threading.Thread(target=self.handle_client, args=(client_conn, client_addr), daemon=True).start()

    def handle_client(self, client_conn, client_addr):
        while True:
            try:
                data = client_conn.recv(1024)
                if not data:
                    break
                # Handle different commands here (not shown for brevity)
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break
        with self.clients_lock:
            self.clients.pop(client_addr, None)  # Remove client from the list upon disconnection
        print(f"Client {client_addr} has disconnected")
        client_conn.close()

    def do_discover(self, hostname):
        "Discover the list of local files of the host named hostname"
        # Use the ping command to check if the hostname exists and is connected
        if self.do_ping(hostname, check_mode=True):  # Added check_mode parameter to ping method
            # If the client is active, proceed to list the shared files
            client_files = self.clients[hostname]['files']
            print(f"Files shared by {hostname}: {client_files}")
        else:
            print(f"Hostname {hostname} is not active or does not exist.")
    
    def do_ping(self, arg, check_mode=False):
        "Check if a host is active: PING <hostname>"
        try:
            # Split the argument by comma and strip any whitespace
            hostname, port_str = arg.split(',')
            hostname = hostname.strip()
            port = int(port_str.strip())  # Convert the port to an integer

            # Create the tuple for client_to_check
            client_to_check = (hostname, port)

            # Lock the clients dictionary to check if the client is active
            with self.clients_lock:
                is_active = any(client_addr[0] == client_to_check[0] and client_addr[1] == client_to_check[1] for client_addr in self.clients)
            
            if check_mode:
                # When called from within another method, return the result instead of printing it
                return is_active
                
            else:
                # Regular ping behavior, print the result
                status = "active" if is_active else "inactive"
                print(f"Client {client_to_check} is {status}")
                # return is_active    
        except ValueError:
            print("Invalid input. Correct format: ping <ip>,<port>")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def do_exit(self, arg):
        "Exit the server shell and shut down the server."
        print("Shutting down server...")
        if self.server_socket:
            self.server_socket.close()
        with self.clients_lock:
            for client_conn in self.clients.values():
                client_conn.close()
            self.clients.clear()
        return True  # Stop the cmd loop
    def do_listclients(self, arg):
        "List all connected clients."
        with self.clients_lock:
            if not self.clients:
                print("No clients are currently connected.")
                return
            for client_addr, client_conn in self.clients.items():
                print(f"Client {client_addr} is connected.")

if __name__ == '__main__':
    host = 'localhost'  # Change to the appropriate interface
    port = 5000  # Change to the appropriate port
    server_cmd = ServerCmd(host, port)
    server_cmd.start_server()
    server_cmd.cmdloop()
