from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'BatmanNinja1'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    migrate.init_app(app,db)
    api.init_app(app)

    from .views import main
    app.register_blueprint(main)

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix = '/api')

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))
