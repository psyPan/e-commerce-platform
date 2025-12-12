from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_store import db
from flask_store.stores.forms import StoreForm
from flask_store.users.models import User
from flask_store.stores.models import Store

stores = Blueprint('stores', __name__)

@stores.route('/add_store', methods=['GET', 'POST'])
def add_store():
    form = StoreForm()
    
    if form.validate_on_submit():
        # Search for user by first name and last name, and check if o_flag is True
        owner = User.query.filter_by(
            f_name=form.owner_f_name.data,
            l_name=form.owner_l_name.data,
            o_flag=True
        ).first()
        
        if not owner:
            flash('Owner not found or the user is not registered as an owner. Please verify the information.', 'danger')
            return render_template('add_store.html', title='New Store', form=form)
        
        # Create new store only if owner exists and is valid
        new_store = Store(
            name=form.store_name.data,
            email=form.email.data,
            phone=form.phone.data,
            balance=0  # Initialize with 0 balance
        )
        
        db.session.add(new_store)
        db.session.flush()  # Flush to get the store.id
        
        # Assign the store_id to the owner
        owner.store_id = new_store.id
        
        # Commit all changes
        db.session.commit()
        
        flash(f'Store {new_store.name} has been created and assigned to {owner.f_name} {owner.l_name}!', 'success')
        return redirect(url_for('home'))  # Redirect to appropriate page
    
    return render_template('add_store.html', title='New Store', form=form)
