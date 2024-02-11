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

organization = Blueprint("organization", __name__)


@organization.before_request
def before_request():
    if session.get("organization") is None:
        return jsonify(
            {"status": "error", "message": "You
        ), 403
        


@organization.route("/post-job", methods=["GET"])
def post_job():
    return render_template("organization/post-job.html")


@organization.route("/api/v2/post-job", methods=["POST"])
def api_post_job():
    request_data = request.json

    approved_fields = [
        "jobtitle",
        "jobdescription",
        "jobexpectedsalaryrangeminimum",
        "jobexpectedsalaryrangemaximum",
        "jobapplicationdeadline",
        "jobsector",
        "jobtype",
        "jobexperience",
        "jobqualification",
        "jobvacancy",
        "jobskill",
        "jobworkplacetype",
        "jobcountry",
        "jobstate",
        "jobcity",
        "jobcompleteaddress",
        "contactname",
        "contactemail",
        "contactphone",
        "alternatephone",
        "contactlinkedin",
    ]

    for approved_field in approved_fields:
        if approved_field not in request_data:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"The request was discarded because the {approved_field.capitalize()} field is missing",
                    }
                ),
                400,
            )

    if request_data["jobapplicationdeadline"] < datetime.now().isoformat():
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The request was discarded because the job application deadline is in the past",
                }
            ),
            400,
        )

    try:
        if int(request_data["jobexpectedsalaryrangeminimum"]) > int(
            request_data["jobexpectedsalaryrangemaximum"]
        ):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "The request was discarded because the minimum salary range is greater than the maximum salary range",
                    }
                ),
                400,
            )

        if int(request_data["jobexpectedsalaryrangeminimum"]) < 0:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "The request was discarded because the minimum salary range is less than 0",
                    }
                ),
                400,
            )

        if int(request_data["jobexpectedsalaryrangemaximum"]) < 0:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "The request was discarded because the maximum salary range is less than 0",
                    }
                ),
                400,
            )

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
                    "message": "The request was discarded because the salary range or vacancy is not a number",
                }
            ),
            400,
        )

    record = {
        "organization_id": session["organization_id"],
        "organization_name": session["organization_name"],
        "organization_logo_url": session["organization_logo_url"],
        "date_posted": datetime.now().isoformat(),
        "is_published": False,
        "application_status": "not-reviewed",
        "applicants": [],
        "approved_applicants": [],
    }

    for approved_field in approved_fields:
        record[approved_field] = request_data[approved_field]

    mongodb_client["jobs"].insert_one(record)

    return jsonify(
        {
            "status": "success",
            "message": "The job application was posted successfully, it will be reviewed by our team and published if it meets our guidelines",
        }
    )
