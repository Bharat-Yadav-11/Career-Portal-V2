from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    flash
)
from config import ApplicationConfig
from datetime import datetime

mongodb_client = ApplicationConfig.mongodb_database

placement = Blueprint("placement", __name__)


@placement.before_request
def before_request():
    if session.get("student") is None:
        return jsonify(
            {"status": "error", "message": "You need to login as a student to access this page"}
        ), 403


@placement.route("/apply-job", methods=["GET"])
def apply_job():
    return render_template("placement/apply-job.html")


@placement.route("/api/v2/apply-job", methods=["POST"])
def api_apply_job():
    request_data = request.json

    mandatory_fields = [
        "jobtitle",
        "jobdescription",
        "jobsector",
        "jobtype",
        "jobexperience",
        "jobqualification",
        "jobvacancy",
        "jobcountry",
        "jobstate",
        "jobcity",
        "contactname",
        "contactemail",
        "contactphone"
    ]

    for field in mandatory_fields:
        if field not in request_data:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"The request was discarded because the {field.capitalize()} field is missing",
                    }
                ),
                400,
            )

    try:
        if int(request_data["jobvacancy"]) < 1:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "The request was discarded because the job vacancy is less than 1",
                    }
                ),
                400,
            )
    except ValueError:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The request was discarded because the job vacancy is not a valid number",
                }
            ),
            400,
        )

    record = {
        "student_id": session["student_id"],
        "student_name": session["student_name"],
        "date_applied": datetime.now().isoformat(),
        "status": "applied"
    }

    for field in mandatory_fields:
        record[field] = request_data[field]

    mongodb_client["applications"].insert_one(record)

    return jsonify(
        {
            "status": "success",
            "message": "Your job application was submitted successfully.",
        }
    )
