from ast import Pass
import cmd
from ipaddress import ip_address
import threading
import socket

from flask import Blueprint, render_template

client = Blueprint('client_real', __name__)

dictionary = "D:/dictionary.txt"
event = threading.Event()
#------------------------------------------------CLIENT SIDE---------------------------------------------------------------------------------#
class ClientShell():
    intro = 'Welcome to the P2P client shell. Type help or ? to list commands.\n'
    prompt = '(client) '

    def __init__(self, ip, port):
        super().__init__()
        self.lock = threading.Lock()
        self.server_ip = ip
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))
          
    def do_exit(self, arg):
        "Exit the client shell"
        print("Exiting client...")
        self.sock.close()
        return True  # Return True to stop the cmd loop and exit

    def do_publish(self, lname, fname, filepath):
        "Inform the server of an existing file\n FORMAT: publish lname fname"
        with open(dictionary, 'a') as file:
            # We have to protect this field cause this is a write-file action
            with self.lock:
                file.write(f"<'{fname}'> <'{filepath}'>\n")
            command = f"publish '{lname}' '{fname}'"
            return self.send_command(self.sock, command)
    
    def do_fetch(self, fname):
        "Request the information of nodes holding specific file from the server\n FORMAT: fetch filename"
        command = f"fetch '{fname}'"
        response = self.send_command(self.sock, command)
        if (response == "2 Error"):
            return f"There is no requested file '{fname}' existed in the network."
            
        elif (response == "3 Error"):
            return f"There is no clients who is holding your requested file '{fname}' be online. Please try again later."
        
        lines = response.split("\n")
        for line in lines:
            # Extract values within angle brackets
            values = [value.strip(" <>") for value in line.split()] # Remove the '<' at the beginning and Remove the '>' at the end
            
            # Get ip_addr and port of the target node
            ip_address = (values[0])
            port = (int)(values[1])
            
            # Establish connection
            p2p_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            p2p_sock.connect((ip_address, port))

            # Send request again
            return self.send_command2(p2p_sock, command)

            break
        
    # This function return the response from the server
    def send_command(self, socket, command):
        try:
            # Send command
            message = command.encode('utf-8')
            socket.sendall(message)

            # Wait for the server's response
            response = socket.recv(4096).decode('utf-8')
            return response

        except Exception as e:
            return f"An error occurred: {e}"
    
    # This function is to handle p2p transfer file
    def send_command2(self, socket, command):
        try:
            # Send command
            message = command.encode('utf-8')
            socket.sendall(message)    
     
            # Receive file
            path = input("Enter the directory for your new downloaded file: ")
            filename = input("Enter the name of your new downloaded file(Don't forget to add the type of your file): ")
            filepath = path + filename
            with open(filepath, 'wb') as file:
                while True:
                    data = socket.recv(256)
                    if not data:
                        break
                    file.write(data)
            return f"The file '{filename}' has been downloaded to your device (path: '{filepath}')."
        except Exception as e:
            return f"An error occurred: {e}"
            


#------------------------------------------------------------------SERVER SIDE--------------------------------------------------------------#
# This class will run parralel with the ClientShell
# But do not print anything, just handle implicitly
class P2P_Server():
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
        threading.Thread(target=self.listen_to_clients, daemon=True).start()

    def listen_to_clients(self):
        while True:
            client_conn, client_addr = self.server_socket.accept()
            with self.clients_lock:
                self.clients[client_addr] = client_conn
            threading.Thread(target=self.handle_client, args=(client_conn, client_addr), daemon=True).start()
            
    def handle_client(self, client_conn, client_addr):
        while True:
            try:
                data = client_conn.recv(1024).decode('utf-8')
                if not data:
                    break
                command = data.strip().split(' ')
                if (command[0] == "fetch"):
                    filename = command[1]
                    self.fetch_file(client_conn, filename)
                else:
                    break
            except ConnectionResetError:
                break
            except Exception as e:
                break
        with self.clients_lock:
            self.clients.pop(client_addr, None)  # Remove client from the list upon disconnection
        client_conn.close()
    
    def send_file(self, socket, file_path):
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(256)
                if not data:
                    break
                socket.sendall(data)
        # Signal the end of file transmission
        socket.shutdown(socket.SHUT_WR)

        
                
    def fetch_file(self, socket, fname):
        with open(dictionary, 'r') as file:
            for line in file:
                # Extract values within angle brackets
                # Remove the '<' at the beginning and Remove the '>' at the end
                values = [value.strip(" <>") for value in line.split()]
                current_fname = values[0]
                filepath = " ".join(values[1:]).strip("'")
                if (current_fname == fname):
                    self.send_file(socket, filepath)
                    break
    

#-----------------------------------------------------------------EXECUTE CODE------------------------------------------------------------------------------#
def run_Server():
    host = 'localhost'  # Change to the appropriate interface
    port = 30  # Change to the appropriate port
    server = P2P_Server(host, port)
    server.start_server()
