from flask import Blueprint

# bluprint untuk user
profileBp = Blueprint("profile", __name__)

from app.profile import routes