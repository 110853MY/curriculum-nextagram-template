from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def loggin():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    password_to_check = request.form.get('password')
    username = request.form.get('username')

    user = User.get_or_none(User.username == username)

    if not user:
        flash("We don't seem to have you in our system. Please doublecheck your name.")
        return redirect(url_for('sessions.new'))

    hashed_password = user.password

    if not check_password_hash(hashed_password, password_to_check):
        flash("That password is incorrect")
        return redirect(url_for('sessions.new'))

    login_user(user)
    flash('Login Successful', 'success')
    return redirect(url_for('home'))


@sessions_blueprint.route("/settings")
@login_required
def settings():
    pass


@sessions_blueprint.route("/logout")
@login_required
def logout():
    logout_user()

    try:
        # session["user_id"] = user.id
        flash('Logout Successful', 'success')
        return redirect(url_for('home'))

    except:
        flash('Logout Failed, you cant leave(remember to call the function for the href)', 'danger')
        return redirect(url_for('home'))


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        return url_for('users.show_feed')
    else:
        return url_for('home')
