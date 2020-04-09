from models.user import User
from models.image import Image
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash


followers_blueprint = Blueprint('followers',
                                __name__,
                                template_folder='templates')


@followers_blueprint.route('/<user_id>/new', methods=['GET'])
@login_required
def new(user_id):
    user = User.get_or_none(User.id == user_id)

    return render_template('followers/new.html', user=user)


@followers_blueprint.route('/<user_id>/')
@login_required
def follow(user_id):
    user = User.get_or_none(User.id == user_id)

    if user is None:
        flash('User{} not found', 'warning')
        return redirect(url_for('users.show_feed'))

    if user == current_user:
        flash('You cannot follow yourself')
        return redirect(url_for('users.show', username=user.username))
        current_user.follow(user)

    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@followers_blueprint.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))
