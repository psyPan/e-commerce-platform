from flask import Blueprint, render_template, request, jsonify, abort, flash, redirect, url_for
from store.models import Store, Product, User, Discount, Review, Order
from store import db
from sqlalchemy import func, or_, and_
from flask_login import login_required, current_user

stores = Blueprint('stores', __name__)

# ============================================
# MAIN STORE VIEW
# ============================================

@stores.route('/store/<int:store_id>')
def view_store(store_id):
    """
    Display a store with its products
    Supports filtering, sorting, and search
    """
    store = Store.query.get_or_404(store_id)
    
    # Get query parameters
    product_type = request.args.get('type')
    manufacturer = request.args.get('manufacturer')
    sort_by = request.args.get('sort', 'newest')
    search_query = request.args.get('q', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock_only = request.args.get('in_stock', 'false').lower() == 'true'
    
    # Base query - only products from this store
    products_query = Product.query.filter_by(store_id=store_id)
    
    # Filter by stock availability
    if in_stock_only:
        products_query = products_query.filter(Product.stock > 0)
    
    # Filter by type (category)
    if product_type:
        products_query = products_query.filter_by(type=product_type)
    
    # Filter by manufacturer
    if manufacturer:
        products_query = products_query.filter_by(manufacturer=manufacturer)
    
    # Search functionality
    if search_query:
        products_query = products_query.filter(
            or_(
                Product.name.ilike(f'%{search_query}%'),
                Product.description.ilike(f'%{search_query}%'),
                Product.model.ilike(f'%{search_query}%')
            )
        )
    
    # Price range filter
    if min_price is not None:
        products_query = products_query.filter(Product.sell_price >= min_price)
    if max_price is not None:
        products_query = products_query.filter(Product.sell_price <= max_price)
    
    # Sorting
    if sort_by == 'price_asc':
        products_query = products_query.order_by(Product.sell_price.asc())
    elif sort_by == 'price_desc':
        products_query = products_query.order_by(Product.sell_price.desc())
    elif sort_by == 'name':
        products_query = products_query.order_by(Product.name.asc())
    elif sort_by == 'discount':
        products_query = products_query.order_by(Product.discount.desc())
    else:  # newest (default)
        products_query = products_query.order_by(Product.product_id.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 12
    products_pagination = products_query.paginate(page=page, per_page=per_page, error_out=False)
    products = products_pagination.items
    
    # Get filter options for dropdowns
    types = db.session.query(Product.type).filter_by(store_id=store_id)\
        .filter(Product.type.isnot(None)).distinct().all()
    types = [t[0] for t in types]
    
    manufacturers = db.session.query(Product.manufacturer)\
        .filter_by(store_id=store_id)\
        .filter(Product.manufacturer.isnot(None)).distinct().all()
    manufacturers = [m[0] for m in manufacturers]
    
    # Get store owners for display
    owners = User.query.filter_by(store_id=store_id, o_flag=True).all()
    
    return render_template('store.html', 
                         store=store,
                         owners=owners,
                         products=products,
                         pagination=products_pagination,
                         types=types,
                         manufacturers=manufacturers,
                         current_filters={
                             'type': product_type,
                             'manufacturer': manufacturer,
                             'sort': sort_by,
                             'search': search_query,
                             'min_price': min_price,
                             'max_price': max_price,
                             'in_stock': in_stock_only
                         })


# ============================================
# STORE DIRECTORY
# ============================================

@stores.route('/stores')
def list_stores():
    """Display all stores with basic info"""
    page = request.args.get('page', 1, type=int)
    per_page = 9
    
    stores_pagination = Store.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Enhance store data with product counts
    store_data = []
    for store in stores_pagination.items:
        product_count = Product.query.filter_by(store_id=store.store_id).count()
        in_stock_count = Product.query.filter(
            Product.store_id == store.store_id,
            Product.stock > 0
        ).count()
        
        store_data.append({
            'store': store,
            'product_count': product_count,
            'in_stock_count': in_stock_count
        })
    
    return render_template('stores_list.html', 
                         stores=store_data,
                         pagination=stores_pagination)


# ============================================
# STORE STATISTICS (for owners/admins)
# ============================================

@stores.route('/store/<int:store_id>/stats')
@login_required
def store_stats(store_id):
    """Get comprehensive statistics for a store"""
    store = Store.query.get_or_404(store_id)
    
    # Check if user is owner or admin
    if not (current_user.a_flag or (current_user.o_flag and current_user.store_id == store_id)):
        abort(403)
    
    # Product statistics
    total_products = Product.query.filter_by(store_id=store_id).count()
    in_stock_products = Product.query.filter(
        Product.store_id == store_id,
        Product.stock > 0
    ).count()
    
    total_inventory = db.session.query(func.sum(Product.stock))\
        .filter_by(store_id=store_id).scalar() or 0
    
    avg_price = db.session.query(func.avg(Product.sell_price))\
        .filter_by(store_id=store_id).scalar() or 0
    
    # Products with active discounts
    discounted_products = Product.query.filter(
        Product.store_id == store_id,
        Product.discount > 0
    ).count()
    
    # Category breakdown
    categories = db.session.query(
        Product.type, 
        func.count(Product.product_id)
    ).filter_by(store_id=store_id)\
     .filter(Product.type.isnot(None))\
     .group_by(Product.type).all()
    
    # Manufacturer breakdown
    manufacturer_counts = db.session.query(
        Product.manufacturer,
        func.count(Product.product_id)
    ).filter_by(store_id=store_id)\
     .filter(Product.manufacturer.isnot(None))\
     .group_by(Product.manufacturer).all()
    
    # Order statistics (if you want to add this)
    # total_orders = Order.query.join(LineItem).join(Product).filter(
    #     Product.store_id == store_id
    # ).distinct().count()
    
    stats = {
        'store_name': store.name,
        'total_products': total_products,
        'in_stock_products': in_stock_products,
        'out_of_stock_products': total_products - in_stock_products,
        'total_inventory_units': int(total_inventory),
        'avg_product_price': round(float(avg_price), 2) if avg_price else 0,
        'discounted_products': discounted_products,
        'balance': float(store.balance) if store.balance else 0.0,
        'categories': [{'name': cat[0], 'count': cat[1]} for cat in categories],
        'manufacturers': [{'name': mfr[0], 'count': mfr[1]} for mfr in manufacturer_counts]
    }
    
    return jsonify(stats)


# ============================================
# PRODUCT DETAILS
# ============================================

@stores.route('/store/<int:store_id>/product/<int:product_id>')
def product_detail(store_id, product_id):
    """View detailed information about a specific product"""
    store = Store.query.get_or_404(store_id)
    product = Product.query.filter_by(
        product_id=product_id,
        store_id=store_id
    ).first_or_404()
    
    # Get related products (same type or manufacturer)
    related_products = Product.query.filter(
        Product.store_id == store_id,
        Product.product_id != product_id,
        or_(
            Product.type == product.type,
            Product.manufacturer == product.manufacturer
        ),
        Product.stock > 0
    ).limit(4).all()
    
    # Get reviews for products from this store (if you want product-specific reviews later)
    # For now, we'll skip this since reviews are tied to orders
    
    return render_template('product_detail.html',
                         store=store,
                         product=product,
                         related_products=related_products)


# ============================================
# FEATURED/DISCOUNTED PRODUCTS
# ============================================

@stores.route('/store/<int:store_id>/deals')
def store_deals(store_id):
    """Show all discounted products in the store"""
    store = Store.query.get_or_404(store_id)
    
    # Get products with discounts
    products = Product.query.filter(
        Product.store_id == store_id,
        or_(
            Product.discount > 0,
            Product.discounted_price.isnot(None)
        ),
        Product.stock > 0
    ).order_by(Product.discount.desc()).all()
    
    return render_template('store_deals.html',
                         store=store,
                         products=products)


# ============================================
# API ENDPOINTS (for AJAX calls)
# ============================================

@stores.route('/api/store/<int:store_id>/products')
def api_get_products(store_id):
    """API endpoint to get products as JSON"""
    store = Store.query.get_or_404(store_id)
    products = Product.query.filter_by(store_id=store_id).all()
    
    return jsonify([{
        'id': p.product_id,
        'name': p.name,
        'price': float(p.sell_price),
        'final_price': float(p.get_final_price()),
        'stock': p.stock,
        'in_stock': p.is_in_stock(),
        'image': p.image,
        'type': p.type,
        'manufacturer': p.manufacturer,
        'discount_percent': float(p.discount) if p.discount else 0
    } for p in products])


@stores.route('/api/store/<int:store_id>/product/<int:product_id>')
def api_get_product(store_id, product_id):
    """API endpoint to get single product as JSON"""
    product = Product.query.filter_by(
        product_id=product_id,
        store_id=store_id
    ).first_or_404()
    
    return jsonify({
        'id': product.product_id,
        'name': product.name,
        'description': product.description,
        'price': float(product.sell_price),
        'discounted_price': float(product.discounted_price) if product.discounted_price else None,
        'final_price': float(product.get_final_price()),
        'discount_percent': float(product.discount) if product.discount else 0,
        'stock': product.stock,
        'in_stock': product.is_in_stock(),
        'image': product.image,
        'type': product.type,
        'manufacturer': product.manufacturer,
        'model': product.model
    })


# ============================================
# QUICK SEARCH (for navbar search)
# ============================================

@stores.route('/search')
def global_search():
    """Search across all stores and products"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return redirect(url_for('stores.list_stores'))
    
    # Search products
    products = Product.query.filter(
        or_(
            Product.name.ilike(f'%{query}%'),
            Product.description.ilike(f'%{query}%'),
            Product.manufacturer.ilike(f'%{query}%')
        )
    ).limit(20).all()
    
    # Search stores
    stores = Store.query.filter(
        or_(
            Store.name.ilike(f'%{query}%'),
            Store.address.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    return render_template('search_results.html',
                         query=query,
                         products=products,
                         stores=stores)