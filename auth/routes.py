from flask import render_template, request, jsonify
from helpers import verify_password_hash, hash_password
from config import ApplicationConfig
from . import auth

mysql_cursor = ApplicationConfig.mysql_client

mysql_cursor = mysql_cursor.cursor()

@auth.route('/sign-in', methods=['GET'])
def sign_in():
    """
    This route is used to render the sign-in page.
    """
    return render_template('auth/sign-in.html')

@auth.route('/api/v2/sign-in', methods=['POST'])
def sign_in_api():
    """
    This route is used to sign-in the user.
    """
    sign_in_data = request.get_json()
    
    if sign_in_data.get('email') is not None and sign_in_data.get('password') is not None:
        mysql_cursor.execute(
            "SELECT * FROM USERS WHERE USER_EMAIL_ADDRESS = %s", (sign_in_data.get('email'),)
        )
        
        user = mysql_cursor.fetchone()
        print(user)

        
        if user is not None:
            print(f"password hash {hash_password(sign_in_data.get('password'))}")
            if verify_password_hash(sign_in_data.get('password'), user['USER_PASSWORD_HASH']):
                return jsonify({"success": True, "message": "The sign-in request was successful"}), 200
            else:
                return jsonify({"success": False, "message": "The email/password combination is incorrect"}), 400
        else:
            return jsonify({"success": False, "message": "The email address is not registered with us"}), 400
    else:
        return jsonify({"success": False, "message": f"The {', '.join([key for key, value in sign_in_data.items() if value is None])} field(s) is/are required"}), 400


@auth.route("/test", methods=["GET"])
def test():
    mysql_cursor.execute("UPDATE USERS SET USER_PASSWORD_HASH = %s WHERE USER_EMAIL_ADDRESS = 'contact@om-mishra.com'", (hash_password(request.args.get('password'))))
    return "Password updated, check the database to verify"
