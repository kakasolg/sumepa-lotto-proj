from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import random
from ..models import db, Game, FavoriteNumber
from .auth import login_required

bp = Blueprint('tickets', __name__, url_prefix='/tickets')


@bp.route('/play/<game_id>')
@login_required
def number_selection(game_id):
    """Page for selecting lottery numbers for a specific game."""
    game = db.session.get(Game, game_id)

    if not game:
        flash('The requested game does not exist.', 'error')
        return redirect(url_for('main.dashboard'))

    # Get user's favorite numbers for this game
    favorite_numbers = FavoriteNumber.query.filter_by(user_id=g.user.id, game_id=game.id).all()

    return render_template('number_selection.html', user=g.user, game=game, favorites=favorite_numbers)

@bp.route('/cart')
@login_required
def cart():
    """Shopping cart view"""
    # In this prototype, the cart is stored in the session
    cart_items = session.get('cart', [])
    
    # Calculate total
    total_price = sum(item['price'] for item in cart_items)

    return render_template('cart.html', user=g.user, cart_items=cart_items, total_price=total_price)

@bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    """Add selected numbers to cart"""
    data = request.get_json()
    game_id = data.get('game_id')
    tickets = data.get('tickets')

    if not game_id or not tickets:
        return jsonify({'success': False, 'message': 'Missing game or ticket data.'}), 400

    game = db.session.get(Game, game_id)
    if not game:
        return jsonify({'success': False, 'message': 'Game not found.'}), 404

    cart = session.get('cart', [])
    
    for ticket in tickets:
        cart.append({
            'game_id': game.id,
            'game_name': game.name,
            'numbers': ticket['numbers'],
            'special_ball': ticket.get(game.special_ball_name.lower().replace(" ", "_") if game.special_ball_name else 'special_ball'),
            'price': game.ticket_price
        })
        
    session['cart'] = cart
    flash(f'{len(tickets)} ticket(s) for {game.name} added to your cart!', 'success')
    return jsonify({'success': True, 'cart_count': len(cart)})

@bp.route('/remove_from_cart/<int:item_index>', methods=['POST'])
@login_required
def remove_from_cart(item_index):
    """Remove an item from the cart"""
    cart = session.get('cart', [])
    if item_index < 0 or item_index >= len(cart):
        return jsonify({'success': False, 'message': 'Invalid cart item index.'}), 400

    # Remove the item
    cart.pop(item_index)
    session['cart'] = cart
    
    flash('Cart item removed.', 'success')
    return jsonify({'success': True, 'cart_count': len(cart)})

# Checkout and Payment Routes

# Define service fees as constants
SERVICE_FEE_PERCENTAGE = 0.10 # 10% service fee
PROCESSING_FEE = 0.50 # $0.50 processing fee

@bp.route('/checkout')
@login_required
def checkout():
    """Checkout process - order review and payment"""
    cart_items = session.get('cart', [])
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Calculate totals
    subtotal = sum(item['price'] for item in cart_items)
    service_fee = subtotal * SERVICE_FEE_PERCENTAGE
    processing_fee = PROCESSING_FEE
    total = subtotal + service_fee + processing_fee
    
    # Check if user needs identity verification
    needs_verification = not g.user.is_identity_verified
    
    return render_template('checkout.html', 
                         user=g.user, cart_items=cart_items,
                         subtotal=subtotal, service_fee=service_fee,
                         processing_fee=processing_fee, total=total,
                         needs_verification=needs_verification)

@bp.route('/process_purchase', methods=['POST'])
@login_required
def process_purchase():
    """Process the purchase (mock implementation)"""
    cart_items = session.get('cart', [])
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # TODO: In production, process actual payment and create real tickets
    # For now, just simulate successful purchase
    
    # Clear cart
    session['cart'] = []
    session.modified = True
    
    flash(f'Purchase successful! You bought {len(cart_items)} ticket(s).', 'success')
    return redirect(url_for('main.my_tickets')) # Redirect to my_tickets page

# API Routes for AJAX calls
@bp.route('/api/quick_pick/<game_id>')
@login_required
def api_quick_pick(game_id):
    """Generate quick pick numbers for a game"""
    game = db.session.get(Game, game_id)
    if not game:
        return jsonify({'error': 'Invalid game'}), 400
    
    # Generate random numbers based on game rules from DB
    main_numbers = sorted(random.sample(range(game.main_numbers_range_low, game.main_numbers_range_high + 1), game.main_numbers_count))
    
    response = {'main_numbers': main_numbers}

    if game.special_ball_name and game.special_ball_range_low and game.special_ball_range_high:
        special_ball = random.randint(game.special_ball_range_low, game.special_ball_range_high)
        response[game.special_ball_name.lower().replace(" ", "_")] = special_ball

    return jsonify(response)
