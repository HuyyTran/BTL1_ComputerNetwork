from flask import Blueprint, render_template, request
from . import client_real

views = Blueprint('views', __name__)

client = None
p2p_server = None

@views.route('/')
def home(): 
    return render_template('index.html')

@views.route('/server')
def server_view():
    return render_template('server.html')

@views.route('/client')
def client_view():
    return render_template('client.html')

@views.route('/connect_server', methods=['GET', 'POST'])
def connect():
    global client
    global p2p_server
    if request.method == "POST":
        try:
            ip = request.form['serverIp']
            port = request.form['serverPort']
            client = client_real.ClientShell(ip, int(port))
            # This function return the port of p2p server
            p2p_server = client_real.P2P_Server('0.0.0.0', 50000).start_server()     

            if client:
                return render_template('client.html', message=f"Connect Successfully for IP Address: {ip} and Port: {port} server!")
        except Exception as e:
            return render_template('client.html', message=f"Error: {e}")
    else:
        return render_template('client.html', message='')

@views.route('/disconnect', methods=['POST'])
def handle_disconnect():
    # Call your Python function here
    client.do_exit()

    # Return a response, could be JSON or just a simple text
    return render_template('client.html', message="You have disconnected from the server.")

@views.route('/publish', methods=['POST'])
def publish():
    if request.method == "POST":
        try:
            lname = request.form['lname']
            fname = request.form['fname']
            filepath = request.form['filepath']

            # Use client_shell to handle publishing logic
            response = client.do_publish(lname, fname, filepath)
            
        except Exception as e:
            response = f"Error: {e}"

        return render_template('client.html', message=response)
    else:
        pass


@views.route('/fetch', methods=['POST'])
def fetch():
    fname = request.form['fname']
    directory = request.form['directory']
    name = request.form['name']
    
    # Use client_shell to handle fetching logic
    response = client.do_fetch(fname, directory, name)
    return response
