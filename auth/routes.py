from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
)
from helpers import verify_password_hash, generate_csrf_token
from config import ApplicationConfig
from datetime import datetime

mongodb_client = ApplicationConfig.mongodb_database

auth = Blueprint("auth", __name__)


@auth.route("/sign-in", methods=["GET"])
def sign_in():
    """
    This route is used to render the sign-in page.
    """
    if session.get("user") is not None:
        return redirect(f"/{session['user']['user_account_redirect_url']}/dashboard")
    return render_template("auth/sign-in.html")


@auth.route("/api/v2/sign-in", methods=["POST"])
def sign_in_api():
    """
    This route is used to sign-in the user.
    """
    sign_in_data = request.get_json()

    if (
        sign_in_data.get("email") is not None
        and sign_in_data.get("password") is not None
    ):
        user = mongodb_client["USERS"].find_one(
            {"user_email_address": sign_in_data.get("email").lower()}
        )
        if user is not None:
            if user["user_account_metadata"]["is_account_blocked"]:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Your account has been blocked, please contact the registrar office.",
                        }
                    ),
                    401,
                )
            if verify_password_hash(
                sign_in_data.get("password"), user["user_hashed_password"]
            ):
                user_redirect_url = ["user", "moderator", "admin"][
                    int(user["user_privilege_level"]) - 1
                ]

                csrf_token = generate_csrf_token()

                session["user"] = {
                    "user_public_id": user["user_public_id"],
                    "user_email_address": user["user_email_address"],
                    "user_privilege_level": user["user_privilege_level"],
                    "user_name": user["user_name"],
                    "user_profile_picture_url": user["user_profile_picture_url"],
                    "user_account_redirect_url": user_redirect_url,
                    "user_session_csrf_token": csrf_token,
                }

                mongodb_client["USERS"].update_one(
                    {"user_public_id": user["user_public_id"]},
                    {"$set": {"user_account_metadata.last_login": datetime.now()}},
                )

                # Send some headers to the client to set the session

                return (
                    jsonify(
                        {
                            "status": "success",
                            "message": "User signed in successfully.",
                            "redirect": f"/{user_redirect_url}",
                        }
                    ),
                    200,
                )

            return (
                jsonify(
                    {"status": "error", "message": "Invalid email address or password."}
                ),
                401,
            )

        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The email address is not registered with us.",
                }
            ),
            400,
        )
    return (
        jsonify(
            {
                "status": "error",
                "message": f"The field(s) {', '.join([field for field in ['email', 'password'] if sign_in_data.get(field) is None])} is/are required.",
            }
        ),
        400,
    )


@auth.route("/sign-out", methods=["GET"])
def sign_out():
    """
    This route is used to sign-out the user.
    """
    if session.get("user") is not None:
        if session["user"]["user_session_csrf_token"] == request.cookies.get(
            "user_session_csrf_token"
        ):
            session.pop("user", None)
        else:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "The request was disallowed due to a missing or invalid CSRF token.",
                    }
                ),
                401,
            )
    return redirect("/auth/sign-in"), 302
