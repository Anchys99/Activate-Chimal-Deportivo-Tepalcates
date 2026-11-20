from flask import Flask, redirect
from flask import Flask
from .config import Config
from .extensions import db, csrf
from .usuarios.routes import usuarios
from .novedades import novedades
from .personal import personal

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(usuarios)


    @app.route("/")
    def inicio():
        return redirect("/novedades/")
    app.register_blueprint(novedades)
    app.register_blueprint(personal)

    return app
