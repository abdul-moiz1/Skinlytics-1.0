from flask import Blueprint

bp = Blueprint('scan', __name__)

from app.scan import routes
