from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    abort
)
from config import ApplicationConfig

mongodb_client = ApplicationConfig.mongodb_database

user = Blueprint("user", __name__)

@user.route("/dashboard", methods=["GET"])
def dashboard():
    if session.get("user") is None:
        return redirect(url_for("auth.sign_in"))
    if session.get("user")["user_privilege_level"] != 1:
        return abort(403)
    """
    This route is used to render the user dashboard.
    """
    return render_template("user/dashboard.html")