from flask import Blueprint

contentBp = Blueprint('content', __name__)

from app.content import routes