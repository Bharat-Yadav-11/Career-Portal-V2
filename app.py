from flask import Flask, request, session

from auth.routes import auth
from config import ApplicationConfig

from tests.database_test import mongodb_test_database, redis_test_database
from helpers import verify_recaptcha_token

app = Flask(__name__)


# Register blueprint(s) for application modules
app.register_blueprint(auth, url_prefix="/auth")

# Application configuration
app.secret_key = ApplicationConfig.secret_key


# Application middleware
@app.before_request
def before_request():
    if request.method == "POST":
        if request.is_json:
            if not verify_recaptcha_token(
                request.json.get("recaptcha_token", ""), ApplicationConfig
            ):
                return {"message": "Invalid reCAPTCHA token"}, 400

@app.after_request
def after_request(response):
    if session.get("user") is not None:
        response.headers["data-csrf-token"] = session["user"]["user_session_csrf_token"]
    return response
            


# Test database connections
mongodb_client = ApplicationConfig.mongodb_client
redis_client = ApplicationConfig.redis_client

if not mongodb_test_database(mongodb_client)[0]:
    raise mongodb_test_database(
        "Unable to connect to MongoDB database"
    )[1]

if not redis_test_database(redis_client)[0]:
    raise redis_test_database(
        "Unable to connect to Redis database"
    )[1]


@app.route("/admin/dashboard", methods=["GET"])
def admin_dashboard():
    return (
        f"The session data is: {session['user']}"
    )


if __name__ == "__main__":
    app.run(debug=ApplicationConfig.app_debug, host=ApplicationConfig.app_host)