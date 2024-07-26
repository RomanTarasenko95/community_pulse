from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.questions import *
from app.models.responses import *
