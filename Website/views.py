from flask import Blueprint, render_template, request, redirect, url_for
from . import client_real
import threading

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
            p2p_server = client_real.P2P_Server('127.0.0.1', 30).start_server()
            

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
    directory = request.form['directory']
    name = request.form['name']
    
    # Use client_shell to handle fetching logic
    response = client.do_fetch(fname, directory, name)
    return response
