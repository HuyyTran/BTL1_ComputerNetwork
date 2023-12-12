from flask import Blueprint, render_template

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

@views.route('/connect_server', methods=['GET', 'POST'])
def connect():
    global client
    if request.method == "POST":
        try:
            ip = request.form['serverIp']
            port = request.form['serverPort']
            client = client_real.ClientShell(ip, int(port))
            
            # Create threads for the P2P client functions
            Server_thread = threading.Thread(target=client_real.run_Server)
            # Start threads
            Server_thread.start()
            if client:
                return render_template('client.html', message=f"Connect Successfully for {ip} and {port} server!")
        except Exception as e:
            return render_template('client.html', message=f"Error: {e}")
    else:
        return render_template('client.html', message='')


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

    # Use client_shell to handle fetching logic
    response = client.do_fetch(fname)

    return response
