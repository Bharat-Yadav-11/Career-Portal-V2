from flask import (
    Blueprint,
    render_template
)
from config import ApplicationConfig

mongodb_client = ApplicationConfig.mongodb_database

user = Blueprint("user", __name__)

@user.route("/dashboard", methods=["GET"])
def dashboard():
    """
    This route is used to render the user dashboard.
    """
    return render_template("user/dashboard.html")