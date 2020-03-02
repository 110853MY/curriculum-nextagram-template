from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.image import Image
from models.image import User
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user


images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html')


@images_blueprint.route('/upload', methods=['POST'])
@login_required
def upload_image():

    if not "user_images" in request.files:
        breakpoint()
        flash('No image has been provided', 'warning')
        return redirect(url_for('images.upload_image'))

    file = request.files.get('user_images')

    file.filename = secure_filename(file.filename)

    if not upload_file_to_s3(file):
        flash('Upload Failed', 'warning')
        return redirect(url_for('images.upload_image'))

    image = Image(user_id=current_user.id, image_name=file.filename)

    image.save()

    flash('Upload Successful', 'success')
    return redirect(url_for('images.upload_image'))
