import os
from flask import Flask

# Aanmaken van globale libraries / extensions  zoals SQLAlchemy, Reddis, etc
# db = SQLAlchemy()

def create_app(config_file="settings.py"):
    # Initialiseren van de 'core application'
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    # print(f" --> KEY: {app.config['SECRET_KEY']}")
    # print(f" --> KEY: {app.config['UPLOAD_FOLDER']}")
    # print(f" --> KEY: {app.config['DE_DATA']}")

    # Initialiseren van plugins / extensions
    # db.init_app(app)

    # Start de app(lication) context
    with app.app_context():
        # Voeg eventuele routes toe:
        # from . import routes # Bijvoorbeeld met '/'
        from .algemeen  import algemeen
        from .gegevens  import gegevens
        from .inlezen   import inlezen
        from .grafieken import grafieken

        # Register Blueprints
        app.register_blueprint(algemeen)
        app.register_blueprint(inlezen.inlezen_bp)
        app.register_blueprint(gegevens.gegevens_bp)
        app.register_blueprint(grafieken.grafieken_bp)

        #print(f"APP: {app.url_map}")

        return app
