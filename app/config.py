import os

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "clave-solo-para-desarrollo-cambiar-en-produccion"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///activate_chimal.db"
    )

    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
