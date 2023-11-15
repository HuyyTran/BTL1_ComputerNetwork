import cmd
import threading
import socket
import json

class ClientShell(cmd.Cmd):
    intro = 'Welcome to the P2P client shell. Type help or ? to list commands.\n'
    prompt = '(client) '

    def __init__(self):
        super().__init__()
        self.server_ip = 'localhost'  # Replace with actual server IP
        self.server_port = 5000       # Replace with actual server port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))
    
   
    
    def do_exit(self, arg):
        "Exit the client shell"
        print("Exiting client...")
        self.sock.close()
        return True  # Return True to stop the cmd loop and exit

    def send_command(self, command):
        try:
            # Send command
            message = json.dumps(command).encode('utf-8')
            self.sock.sendall(message)

            # Wait for the server's response
            response = self.sock.recv(4096).decode('utf-8')
            print(f"Server response: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")

def run_shell():
    shell = ClientShell()
    shell.cmdloop()

if __name__ == '__main__':
    shell_thread = threading.Thread(target=run_shell)
    shell_thread.start()
