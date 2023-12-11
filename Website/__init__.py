from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager

# init the database
#db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #app configuration
    app.config['SECRET_KEY'] = 'abc'
    ##############################

    
    #init the database with app 
    #db.init_app(app)
    ##############################

    from .views import views
    from .client_real import client
    from .server_real import server

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(client, url_prefix = '/')
    app.register_blueprint(server, url_prefix = '/')

    return app



