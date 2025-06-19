# LottoGo - California Lottery Courier Service Prototype
# Main Flask application file

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
import random

# Import mock data
from mockdata import (
    TEST_USERS, GAMES, MOCK_TICKETS, FAVORITE_NUMBERS, SERVICE_FEES,
    get_user_by_email, get_user_tickets, get_user_favorites, simulate_ticket_lifecycle
)

app = Flask(__name__)
app.secret_key = 'lottogo_dev_secret_key_2025'  # TODO: Use environment variable in production

# Helper functions
def is_logged_in():
    """Check if user is logged in"""
    return 'user_id' in session

def get_current_user():
    """Get current logged in user data"""
    if is_logged_in():
        user_id = session['user_id']
        for user in TEST_USERS.values():
            if user['id'] == user_id:
                return user
    return None

def require_login():
    """Decorator to require login for protected routes"""
    if not is_logged_in():
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    return None

# Landing and Authentication Routes
@app.route('/')
def landing():
    """Landing page for non-logged in users"""
    if is_logged_in():
        return redirect(url_for('dashboard'))
    
    # Mock jackpot data for landing page
    featured_games = [
        GAMES['mega_millions'],
        GAMES['powerball'],
        GAMES['superlotto_plus']
    ]
    
    return render_template('landing.html', games=featured_games)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if is_logged_in():
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # TODO: In production, use proper password hashing
        user = get_user_by_email(email)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if is_logged_in():
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # TODO: In production, implement proper user registration
        # with email verification, password hashing, etc.
        flash('Registration is not available in this prototype. Use demo@lottogo.com / demo123', 'info')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('landing'))

# Main Dashboard and Navigation
@app.route('/dashboard')
def dashboard():
    """Main dashboard - Play tab"""
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()
    
    # Simulate ticket lifecycle updates
    simulate_ticket_lifecycle()
    
    # Get all games for dashboard
    games_list = list(GAMES.values())
    
    return render_template('dashboard.html', user=user, games=games_list, active_tab='play')

@app.route('/tickets')
def tickets():
    """Tickets tab - user's purchased tickets"""
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()
    
    # Update ticket lifecycle before showing
    simulate_ticket_lifecycle()
    
    # Get user tickets by status (excluding archived)
    active_tickets = get_user_tickets(user['id'], 'active')
    checked_tickets = get_user_tickets(user['id'], 'checked')
    
    return render_template('tickets.html', user=user, 
                         active_tickets=active_tickets, 
                         checked_tickets=checked_tickets,
                         active_tab='tickets')

@app.route('/account')
def account():
    """Account tab - user profile and settings"""
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()
    
    return render_template('account.html', user=user, active_tab='account')

# Game and Shopping Routes
@app.route('/play/<game_id>')
def number_selection(game_id):
    """Number selection screen for specific game"""
    login_check = require_login()
    if login_check:
        return login_check
    
    if game_id not in GAMES:
        flash('Game not found.', 'error')
        return redirect(url_for('dashboard'))
    
    game = GAMES[game_id]
    user = get_current_user()
    favorites = get_user_favorites(user['id'])
    
    # Filter favorites for this game
    game_favorites = [fav for fav in favorites if fav['game'] == game_id]
    
    return render_template('number_selection.html', 
                         game=game, user=user, favorites=game_favorites)

@app.route('/cart')
def cart():
    """Shopping cart view"""
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()
    
    # Get cart items from session
    cart_items = session.get('cart', [])
    
    # Calculate totals
    subtotal = sum(item['price'] for item in cart_items)
    service_fee = subtotal * SERVICE_FEES['service_fee_percentage']
    processing_fee = SERVICE_FEES['processing_fee']
    total = subtotal + service_fee + processing_fee
    
    return render_template('cart.html', 
                         user=user, cart_items=cart_items,
                         subtotal=subtotal, service_fee=service_fee,
                         processing_fee=processing_fee, total=total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add selected numbers to cart"""
    login_check = require_login()
    if login_check:
        return login_check
    
    # TODO: In production, validate all input data
    game_id = request.form.get('game_id')
    numbers = request.form.get('numbers')
    special_number = request.form.get('special_number')
    
    if game_id not in GAMES:
        flash('Invalid game selection.', 'error')
        return redirect(url_for('dashboard'))
    
    game = GAMES[game_id]
    
    # Create cart item
    cart_item = {
        'id': f"cart_{len(session.get('cart', []))}",
        'game_id': game_id,
        'game_name': game['name'],
        'numbers': numbers,
        'special_number': special_number,
        'price': game['ticket_price'],
        'draw_date': game['next_draw']
    }
    
    # Add to session cart
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(cart_item)
    session.modified = True
    
    flash(f'Added {game["name"]} ticket to cart!', 'success')
    return redirect(url_for('cart'))

# Checkout and Payment Routes
@app.route('/checkout')
def checkout():
    """Checkout process - order review and payment"""
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()
    cart_items = session.get('cart', [])
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('dashboard'))
    
    # Calculate totals
    subtotal = sum(item['price'] for item in cart_items)
    service_fee = subtotal * SERVICE_FEES['service_fee_percentage']
    processing_fee = SERVICE_FEES['processing_fee']
    total = subtotal + service_fee + processing_fee
    
    # Check if user needs identity verification
    needs_verification = not user['is_identity_verified']
    
    return render_template('checkout.html', 
                         user=user, cart_items=cart_items,
                         subtotal=subtotal, service_fee=service_fee,
                         processing_fee=processing_fee, total=total,
                         needs_verification=needs_verification)

@app.route('/process_purchase', methods=['POST'])
def process_purchase():
    """Process the purchase (mock implementation)"""
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()
    cart_items = session.get('cart', [])
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('dashboard'))
    
    # TODO: In production, process actual payment and create real tickets
    # For now, just simulate successful purchase
    
    # Clear cart
    session['cart'] = []
    session.modified = True
    
    flash(f'Purchase successful! You bought {len(cart_items)} ticket(s).', 'success')
    return redirect(url_for('tickets'))

# API Routes for AJAX calls
@app.route('/api/quick_pick/<game_id>')
def api_quick_pick(game_id):
    """Generate quick pick numbers for a game"""
    if game_id not in GAMES:
        return jsonify({'error': 'Invalid game'}), 400
    
    game = GAMES[game_id]
    
    # Generate random numbers based on game rules
    if game_id == 'powerball':
        main_numbers = sorted(random.sample(range(1, 70), 5))
        powerball = random.randint(1, 26)
        return jsonify({
            'main_numbers': main_numbers,
            'powerball': powerball
        })
    elif game_id == 'mega_millions':
        main_numbers = sorted(random.sample(range(1, 71), 5))
        mega_ball = random.randint(1, 25)
        return jsonify({
            'main_numbers': main_numbers,
            'mega_ball': mega_ball
        })
    elif game_id == 'superlotto_plus':
        main_numbers = sorted(random.sample(range(1, 48), 5))
        mega_number = random.randint(1, 27)
        return jsonify({
            'main_numbers': main_numbers,
            'mega_number': mega_number
        })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Development server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
