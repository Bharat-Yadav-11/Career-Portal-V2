from flask import render_template, redirect, url_for, request, flash
from . import auth

@auth.route('/sign-in', methods=['GET'])
def sign_in():
    """
    This route is used to render the sign-in page.
    """
    return render_template('sign-in.html')