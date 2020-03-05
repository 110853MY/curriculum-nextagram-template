from models.user import User
from models.image import Image
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from instagram_web.util.braintree import gateway

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')


@donations_blueprint.route('/<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)

    client_token = gateway.client_token.generate()

    if not client_token:
        flash('Unable to obtain token', 'warning')
        return redirect(url_for('users.show_feed'))

    return render_template('donations/new.html', image=image,
                           client_token=client_token)


@donations_blueprint.route('/<image_id>/', methods=['POST'])
@login_required
def create(image_id):
    nonce = request.form.get('payment_method_nonce')
    breakpoint()
    if not nonce:
        flash('Invalid credsit card details', 'warning')
        return redirect(url_for('users.show_feed'))

    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash('No image found with provided id', 'warning')
        return redirect(url_for('users.show_feed'))

    amount = request.form.get('amount')

    if not amount:
        flash('No donation amount provided', 'warning')
        return redirect(url_for('user.show_feed'))
    breakpoint()
    result = gateway.transaction.sale({
        "amount": amount,
        'payment_method_nonce': nonce,
        'options': {
            "submit_for_settlement": True
        }
    })
    breakpoint()
    if not result.is_success:
        flash('Unable to complete transaction', 'warning')
        return redirect(url_for('users.show_feed'))

    donation = Donation(amount=amount, image_id=image.id,
                        user_id=current_user.id)

    if not donation.save():
        flash('Donation succesful but error creating record', 'warning')
        return redirect(url_for('users.show_feed'))

    flash('Successfully donated RM{amount}', 'success')
    return redirect(url_for('users.show_feed'))
