import cmd
import threading
import socket

dictionary = "D:/dictionary_s.txt"
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
                data = client_conn.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Client ({client_addr}): " + data + "\n")
                host, port = client_addr
                command = data.strip().split(' ')
                flag = 0
                # Handle 'publish' command from client
                # Remind syntax: publish lname fname
                if (command[0] == "publish"):
                    with open(dictionary, 'a') as file:
                        with self.clients_lock:
                            file.write(f"<'{host}'> <'{port}'> <'{command[2]}'>\n")
                    flag = 1
                    response = "1 OK"
                elif (command[0] == "fetch"):
                    print("fetching...")
                    # Loop the dictionary to find fname and its corespoding hostname
                    with open(dictionary, 'r') as file:
                        for line in file:
                            values = [value.strip(" <>") for value in line.split()]
                            ip = values[0].strip("'")
                            port = values[1].strip("'")
                            hostname = ip + "," + port
                            fname = " ".join(values[2:]).strip("'")
                            if (fname == command[1].strip("'")):
                                if (self.do_ping(hostname, check_mode=True)):                               
                                    response = f"<{ip}> <{port}>"
                                    flag = 1
                                    break
                                else:
                                    flag = 2  
                        if (flag == 0):
                            response = "2 Error"
                        elif(flag == 2):
                            response = "3 Error"
                message = response.encode('utf-8')
                client_conn.sendall(message)
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

    # def do_discover(self, hostname):
    #     "Discover the list of local files of the host named hostname"
    #     # Use the ping command to check if the hostname exists and is connected
    #     if self.do_ping(hostname, check_mode=True):  # Added check_mode parameter to ping method
    #         # If the client is active, proceed to list the shared files
    #         client_files = self.clients[hostname]['files']
    #         print(f"Files shared by {hostname}: {client_files}")
    #     else:
    #         print(f"Hostname {hostname} is not active or does not exist.")
    
    def parse_dictionary_s(self,contents):
        files_dictionary = {}
        lines = contents.strip().splitlines()
        for line in lines:
        # Remove the angle brackets and extra single quotes
            parts = line.translate(str.maketrans('', '', "<>'")).split()
            if len(parts) == 3:
                address, port, file_name = parts
                port = int(port)  # Convert the port to an integer
                key = (address, port)
                if key not in files_dictionary:
                    files_dictionary[key] = []
                files_dictionary[key].append(file_name)
        return files_dictionary

    def load_shared_files_dictionary(self):
        # Load and parse the contents of dictionary_s.txt
        with open('D:/dictionary_s.txt', 'r') as file:
            contents = file.read()
        return self.parse_dictionary_s(contents)
    
    def do_discover(self, arg):
        "Discover the list of local files of the host named by address and port"
        # Load the shared files from the dictionary
        files_dictionary = self.load_shared_files_dictionary()
        
        # Parse the argument to get the address and port
        try:
            address, port_str = arg.split(',')
            port = int(port_str)
            client_key = (address, port)
            
            # Find the files shared by the specified client
            if client_key in files_dictionary:
                files_list = files_dictionary[client_key]
                print(f"Files shared by {client_key}: {files_list}")
            else:
                print(f"No files shared by {client_key} or client not connected.")
        except ValueError:
            print(f"Incorrect format for discover command. Expected format: discover <address>,<port>")

    
    
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
