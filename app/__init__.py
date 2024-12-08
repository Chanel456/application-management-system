import logging
from flask import Flask, render_template, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from os import path

from werkzeug.utils import redirect


from config.config import Config

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app(config_class=Config):
    """Initialises the flask app with config, registers the blueprints and, initialises the login manager """

    app.config.from_object(config_class)
    logging.basicConfig(level= logging.INFO, format = f'%(asctime)s - %(levelname)s : %(message)s')
    db.init_app(app)

    #Import routes
    from app.views import views
    from app.auth import auth
    from app.application import application
    from app.server import server

    #Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(application, url_prefix='/application')
    app.register_blueprint(server, url_prefix='/server')

    from app.models.user import User
    from app.models.application import create_applications
    from app.models.server import create_servers

    with app.app_context():
        if not path.exists('app/' + DB_NAME):
            db.create_all()
            logging.info('Database created')

    # Initialise login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

@app.route('/')
def redirect_to_home():
    """Redirects base url to the dashboard html"""
    return redirect(url_for('views.dashboard'))

@app.errorhandler(404)
def handle_not_found_error(err):
    """Redirects to 404.html if a HTTP 404 error is thrown"""
    return render_template('error/404.html', user=current_user), 404

@app.errorhandler(500)
def handle_internal_server_error(err):
    """Redirects to 500.html if a 500 error is thrown"""
    return render_template('error/500.html', user=current_user), 500