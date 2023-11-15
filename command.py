import cmd
import threading
#This file doesn't attribute to the assignment
#It just shows how basic CLI work
class ServerShell(cmd.Cmd):
    intro = 'Welcome to the server shell. Type help or ? to list commands.\n'
    prompt = '(server) '

    def do_discover(self, arg):
        "Discover files shared by a host: DISCOVER <hostname>"
        # Call the server method to handle the 'discover' action
        print(arg)

    def do_ping(self, arg):
        "Check if a host is active: PING <hostname>"
        # Call the server method to handle the 'ping' action

    def do_exit(self, arg):
        "Exit the server shell"
        print("Shutting down server...")
        return True  # Return True to stop the cmd loop and exit

def run_shell():
    shell = ServerShell()
    shell.cmdloop()


if __name__ == '__main__':
    # ServerShell().cmdloop()
    shell_thread = threading.Thread(target=run_shell)
    shell_thread.start()
