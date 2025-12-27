from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flask_store import db
from flask_store.discounts.forms import DiscountForm
from flask_store.discounts.models import Discount

discounts = Blueprint('discounts', __name__)

@discounts.route('/add_discount', methods=['GET', 'POST'])
@login_required
def add_discount():
    if current_user.c_flag:
        flash('You do not have permission to this page', 'danger')
        return redirect(url_for('users.home'))
    form = DiscountForm()
    page = request.args.get('page', 1, type=int)
    discounts_pagination = Discount.query.paginate(
        page=page, 
        per_page=5, 
        error_out=False
    )
    if form.validate_on_submit():
        if form.save.data:
            discount = Discount(
                name=form.name.data,
                code=form.code.data,
                description=form.description.data,
                type=form.type.data,
                discount_percent=form.discount_percent.data,
                creator_id=current_user.id
            )
            try:
                db.session.add(discount)
                db.session.commit()
                flash(f'Discount "{discount.name}" created successfully!', 'success')
                return redirect(url_for('discounts.add_discount'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating the discount.', 'danger')
                return render_template('owner/add_discount.html', form=form)
        elif form.cancel.data:
            return redirect(url_for('users.home'))
    return render_template('owner/add_discount.html', title='Add Discount', form=form, discounts=discounts_pagination.items, pagination=discounts_pagination)