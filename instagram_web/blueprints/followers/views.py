from models.user import User
from models.image import Image
from models.follower_following import FollowerFollowing
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash


followers_blueprint = Blueprint('followers',
                                __name__,
                                template_folder='templates')


@followers_blueprint.route('/<idols_id>', methods=['POST'])
@login_required
def create(idols_id):

    idol = User.get_or_none(User.id == idols_id)

    if not idol:
        flash('No user found with this id!')
        return redirect(url_for('users.show_feed'))

    new_follow = FollowerFollowing(
        fans_id=current_user.id,
        idols_id=idol.id
    )

    if not new_follow.save():
        flash('Unable to follow this user!')
        return render_template('followers/new.html', user=idols_id)

    else:
        flash(f'You are now following {idol.username}')
        return redirect(url_for('users.show_feed', username=idol.username))

    flash('Follow request send! Please wait for approval!')
    return redirect(url_for('users.show_feed', username=idol.username))


@followers_blueprint.route('/<idol_id>/delete', methods=['POST'])
@login_required
def delete(idol_id):

    follow = FollowerFollowing.get_or_none((FollowerFollowing.idols_id == idols_id) and (
        FollowerFollowing.fan_id == current_user.id))

    if follow.delete_instance():
        flash(f'You have unfollowed{follow.idol.username}')
        return redirect(url_for('users.show_feed', username=follow.idol.username))
