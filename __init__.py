from flask import Flask 
from.extensions import base_alerta,migrate
from.routes.alertaBp import alertaBp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_alerta.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    base_alerta.init_app(app)
    migrate.init_app(app)

    app.register_blueprint(alertaBp)
    
    return app