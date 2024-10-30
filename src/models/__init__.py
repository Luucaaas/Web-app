from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .client import Client
from .meeting import Meeting
