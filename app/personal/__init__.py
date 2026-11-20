from flask import Blueprint

personal = Blueprint(
    "personal",
    __name__,
    url_prefix="/personal"
)

from . import routes
