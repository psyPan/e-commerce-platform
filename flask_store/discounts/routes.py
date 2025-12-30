from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flask_store import db
from flask_store.discounts.forms import DiscountForm
from flask_store.discounts.models import Discount, Shipping, Seasoning, SpecialEvent
from datetime import datetime

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

@discounts.route('/discount/delete/<int:discount_id>')
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

@discounts.route('/discount/edit/<int:discount_id>', methods=['POST'])
@login_required
def edit_discount(discount_id):
    """Edit discount details (Owner only)"""
    discount = Discount.query.get_or_404(discount_id)
    
    # Check if user is owner of this discount's store
    if not current_user.o_flag or current_user.store_id != discount.store_id:
        flash('You do not have permission to edit this discount', 'danger')
        return redirect(url_for('discounts.add_discount'))
    
    try:
        # Update basic discount fields
        discount.name = request.form.get('name')
        discount.code = request.form.get('code')
        discount.description = request.form.get('description')
        discount.discount_percent = float(request.form.get('discount_percent'))
        
        # Update active status
        discount.is_active = request.form.get('is_active') == '1'
        
        old_type = discount.type
        new_type = request.form.get('type')
        
        # If type changed, delete old type-specific details
        if old_type != new_type:
            if old_type == 'shipping' and discount.shipping_details:
                db.session.delete(discount.shipping_details)
            elif old_type == 'seasoning' and discount.seasoning_details:
                db.session.delete(discount.seasoning_details)
            elif old_type == 'special_event' and discount.special_event_details:
                db.session.delete(discount.special_event_details)
            
            discount.type = new_type
            db.session.flush()
        
        # Handle type-specific fields
        if new_type == 'shipping':
            min_purchase = request.form.get('min_purchase')
            if min_purchase:
                if discount.shipping_details:
                    discount.shipping_details.min_purchase = float(min_purchase)
                else:
                    shipping = Shipping(
                        discount_id=discount.id,
                        min_purchase=float(min_purchase)
                    )
                    db.session.add(shipping)
                
        elif new_type == 'seasoning':
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            if start_date_str and end_date_str:
                # Convert strings to date objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                
                if discount.seasoning_details:
                    discount.seasoning_details.start_date = start_date
                    discount.seasoning_details.end_date = end_date
                else:
                    seasoning = Seasoning(
                        discount_id=discount.id,
                        start_date=start_date,
                        end_date=end_date
                    )
                    db.session.add(seasoning)
                
        elif new_type == 'special_event':
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            if start_date_str and end_date_str:
                # Convert strings to date objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                
                if discount.special_event_details:
                    discount.special_event_details.start_date = start_date
                    discount.special_event_details.end_date = end_date
                else:
                    special_event = SpecialEvent(
                        discount_id=discount.id,
                        start_date=start_date,
                        end_date=end_date
                    )
                    db.session.add(special_event)
        
        db.session.commit()
        
        status_msg = "activated" if discount.is_active else "deactivated"
        flash(f'Discount updated and {status_msg} successfully!', 'success')
    except ValueError as e:
        db.session.rollback()
        flash(f'Invalid date format. Please use YYYY-MM-DD format.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating discount: {str(e)}', 'danger')
    
    return redirect(url_for('discounts.add_discount'))