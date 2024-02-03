import requests
import bcrypt
    
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

def verify_password_hash(password: str, password_hash: str) -> bool:
    """
    Verify a password against a password hash
    :param password: The password to verify
    :param password_hash: The password hash to verify against
    :return: True if the password is valid, False otherwise
    """
    if bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
        print("password is correct")
    else:
        print("password is incorrect")
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    :param password: The password to hash
    :return: The hashed password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())