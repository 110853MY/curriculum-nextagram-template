from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models.user import User
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():

    users_password = request.form.get('password')
    hashed_password = generate_password_hash(users_password)

    email = request.form.get('email')
    username = request.form.get('username')

    signup = User(email=email, username=username, password=hashed_password)

    try:
        signup.save()
        user = User.get_or_none(User.username == username)
        login_user(user)
        flash('User successfully signed up', 'success')
        return redirect(url_for('home', username=user.username))

    except:
        flash('Error creating User', 'danger')
        return redirect(url_for('users.new'))


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.username == username)

    if not user:
        flash('No user found with provided ID', 'warning')
        return redirect(url_for('users.show'))

    return render_template('users/edit.html', user=user)


@users_blueprint.route('/<username>/', methods=["POST"])
@login_required
def edit_username(username):

    user = User.get_or_none(User.username == username)

    new_username = request.form.get('username')
    user.username = new_username

    try:
        user.save()
        flash('Username updated successful', 'success')
        return redirect(url_for('home', username=user.username))

    except:
        flash('Unable to update username', 'warning')
        return redirect(url_for('home', username=user.username))


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
