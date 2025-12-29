from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flask_store import db
from flask_store.discounts.forms import DiscountForm
from flask_store.discounts.models import Discount, Shipping, Seasoning, SpecialEvent

discounts = Blueprint('discounts', __name__)

@discounts.route('/add_discount', methods=['GET', 'POST'])
@login_required
def add_discount():
    if current_user.c_flag:
        flash('You do not have permission to this page', 'danger')
        return redirect(url_for('users.home'))
    if not current_user.store_id:
        flash('You need to create a store first', 'danger')
        return redirect(url_for('stores.store_info'))
    form = DiscountForm()
    page = request.args.get('page', 1, type=int)

    search_query = request.args.get('search', '')
    filter_by = request.args.get('filter_by', 'all')
    # Filter by current user's store only
    query = Discount.query.filter_by(store_id=current_user.store_id)
    # Apply search filter
    if search_query:
        query = query.filter(Discount.name.contains(search_query))
    
    # Apply filters
    if filter_by == 'active':
        query = query.filter(Discount.is_active == True)
    elif filter_by == 'inactive':
        query = query.filter(Discount.is_active == False)

    discounts_pagination = query.paginate(page=page, per_page=5, error_out=False)
    discounts = discounts_pagination.items
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
                db.session.flush()
                if discount.type == 'shipping':
                    shipping = Shipping(
                        discount_id=discount.id,
                        min_purchase=form.min_purchase.data
                    )
                    db.session.add(shipping)
                    
                elif discount.type == 'seasoning':
                    seasoning = Seasoning(
                        discount_id=discount.id,
                        start_date=form.start_date.data,
                        end_date=form.end_date.data
                    )
                    db.session.add(seasoning)
                    
                elif discount.type == 'special_event':
                    special_event = SpecialEvent(
                        discount_id=discount.id,
                        start_date=form.start_date.data,
                        end_date=form.end_date.data
                    )
                    db.session.add(special_event)
                db.session.commit()
                flash(f'Discount "{discount.name}" created successfully!', 'success')
                return redirect(url_for('discounts.add_discount'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating the discount.', 'danger')
                return render_template('owner/add_discount.html', form=form)
        elif form.cancel.data:
            return redirect(url_for('users.home'))
    return render_template('owner/add_discount.html', title='Add Discount', form=form, discounts=discounts, pagination=discounts_pagination)

@discounts.route('/delete/<int:discount_id>')
@login_required
def delete_discount(discount_id):
    discount = Discount.query.get_or_404(discount_id)
    
    # Check ownership
    if current_user.store_id != discount.store_id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('discounts.add_discount'))
    discount.is_active = False
    db.session.commit()
    
    flash('Discount deleted successfully', 'success')
    return redirect(url_for('discounts.add_discount'))