from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'abc'

    from .views import views
    # from .client_real import client
    # from .server_real import server

    app.register_blueprint(views, url_prefix = '/')
    # app.register_blueprint(client, url_prefix = '/')
    # app.register_blueprint(server, url_prefix = '/')

    return app



