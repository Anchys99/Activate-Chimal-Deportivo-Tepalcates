from flask import Blueprint

novedades = Blueprint(
    "novedades",
    __name__,
    url_prefix="/novedades"
)

from . import routes
