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
    password_to_check = request.form['password']
    hashed_password = User.password
    result = check_password_hash(hashed_password, password_to_check)

    username = request.form.get('username')

    try:
        if username == 'username' and result == 'password':
            flash('Login Successfull', 'success')
            return redirect(url_for('home'))

    except:
        flash('Login Failed', 'danger')
        return redirect(url_for('sessions.new'))
