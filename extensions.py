from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# instanciando os objetos
base_alerta = SQLAlchemy()
migrate = Migrate()

