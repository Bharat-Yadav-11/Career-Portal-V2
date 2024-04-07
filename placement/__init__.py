from flask import Blueprint

auth = Blueprint('placement', __name__)

# Import the routes after creating the blueprint to avoid circular imports
from . import routes