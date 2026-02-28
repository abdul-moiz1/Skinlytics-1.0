from flask import Blueprint

bp = Blueprint('recommendation', __name__)

from app.recommendation import routes
