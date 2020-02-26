from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from models.user import User

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def login():

    password_to_check = request.form.get('password')
    username = request.form.get('username')

    user = User.get_or_none(User.username == username)
    hashed_password = user.password

    if not user:
        flash("We don't seem to have you in our system. Please doublecheck your name.")

    if not check_password_hash(hashed_password, password_to_check):
        flash("That password is incorrect")

    try:
        session["user_id"] = user.id
        flash('Login Successfull', 'success')
        return redirect(url_for('home'))

    except:
        flash('Login Failed', 'danger')
        return redirect(url_for('sessions.new'))
