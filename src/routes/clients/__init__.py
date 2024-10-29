from flask import Blueprint

client_bp = Blueprint("clients",__name__)

from src.routes.clients import routes
