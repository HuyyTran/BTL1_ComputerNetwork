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