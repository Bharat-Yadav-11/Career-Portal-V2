import json

from flask import Flask, request, session, jsonify, render_template
from flask_session import Session


from auth.routes import auth
from user.routes import user
from organization.routes import organization
from config import ApplicationConfig

from tests.database_test import mongodb_test_database, redis_test_database
from helpers import verify_recaptcha_token

app = Flask(__name__)

# Session configuration

app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = ApplicationConfig.redis_client
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "session:"
Session(app)

# Register blueprint(s) for application modules
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(organization, url_prefix="/organization")

# Application configuration
app.secret_key = ApplicationConfig.secret_key


# Application middleware
@app.before_request
def before_request():
    if request.method == "POST":
        if request.is_json:
            if not verify_recaptcha_token(
                request.json.get("reCaptchaToken", ""), ApplicationConfig
            ):
                return {
                    "message": "The request was aborted because the reCAPTCHA token was invalid"
                }, 403


@app.before_request
def before_request():
    if session.get("user") is not None:
        if request.method in ["POST", "PUT", "DELETE"]:
            if (
                request.headers.get("X-Career-Portal-CSRF-Token")
                != session["user"]["user_session_csrf_token"]
            ):
                return {
                    "message": "The operation was aborted because the request did not contain a valid CSRF token"
                }, 403


@app.after_request
def after_request(response):
    if session.get("user") is not None:
        response.set_cookie(
            "user_session_csrf_token",
            session["user"]["user_session_csrf_token"],
            secure=True,
        )
    return response


# Test database connections
mongodb_client = ApplicationConfig.mongodb_client
redis_client = ApplicationConfig.redis_client

if not mongodb_test_database(mongodb_client)[0]:
    raise mongodb_test_database("Unable to connect to MongoDB database")[1]

if not redis_test_database(redis_client)[0]:
    raise redis_test_database("Unable to connect to Redis database")[1]


# Application routes


@app.route("/admin/dashboard", methods=["GET"])
def admin_dashboard():
    return f"The session data is: {session['user']}"


@app.errorhandler(403)
def forbidden(e):
    return (
        jsonify(
            {
                "status": "error",
                "message": "Unsufficient privileges to access this resource",
            }
        ),
        403,
    )


if __name__ == "__main__":
    app.run(debug=ApplicationConfig.app_debug, host=ApplicationConfig.app_host)
