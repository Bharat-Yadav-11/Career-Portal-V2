import bcrypt
import requests
import secrets

def generate_csrf_token():
    """
    Generate a CSRF token
    :return: The CSRF token
    """
    return secrets.token_urlsafe(32)

def verify_recaptcha_token(token: str, ApplicationConfig: object) -> bool:
    """
    Verify a reCAPTCHA token using the Google reCAPTCHA API
    :param token: The reCAPTCHA token to verify
    :return: True if the token is valid, False otherwise
    """


    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": ApplicationConfig.recaptcha_secret_key,
            "response": token,
        },
    timeout=5
    )

    return response.json().get("success", False)

def verify_password_hash(password, password_hash):
    """
    Verify a password against a password hash
    :param password: The password to verify
    :param password_hash: The password hash to verify against
    :return: True if the password is valid, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash)

def hash_password(password):
    """
    Hash a password
    :param password: The password to hash
    :return: The hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

