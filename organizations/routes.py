from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
)
from config import ApplicationConfig
from datetime import datetime

mongodb_client = ApplicationConfig.mongodb_database

organization = Blueprint("organization", __name__)


@organization.route("/post-job", methods=["GET"])
def post_job():
    return render_template("organization/post-job.html")


@organization.route("/api/v1/organization/post-job", methods=["POST"])
def api_post_job():
    request_data = request.json
    print(request_data)
    return (
        jsonify(
            {"status": "error", "message": "This feature is currently not available"}
        ),
        501,
    )
