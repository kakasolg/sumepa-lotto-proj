# LottoGo - California Lottery Courier Service Prototype
# Main Flask application file

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
import random
import click

# Import database models and db instance
from models import db, User, Game, Ticket, FavoriteNumber

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottogo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'lottogo_dev_secret_key_2025'  # TODO: Use environment variable in production

# Initialize the database
db.init_app(app)

# --- CLI Commands for DB management ---
@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    with app.app_context():
        db.create_all()
    click.echo("Initialized the database.")

@app.cli.command("seed-db")
def seed_db_command():
    """Seeds the database with mock data."""
    with app.app_context():
        # Clear existing data
        db.session.query(FavoriteNumber).delete()
        db.session.query(Ticket).delete()
        db.session.query(User).delete()
        db.session.query(Game).delete()
        
        # Seed Users
        from mockdata import TEST_USERS
        for user_data in TEST_USERS.values():
            new_user = User(
                id=user_data['id'],
                email=user_data['email'],
                name=user_data['name'],
                phone=user_data['phone'],
                password=user_data['password'], # In real app, hash this
                is_identity_verified=user_data['is_identity_verified'],
                wallet_balance=user_data['wallet_balance']
            )
            db.session.add(new_user)
            
        # Seed Games
        from mockdata import GAMES
        for game_id, game_data in GAMES.items():
            new_game = Game(
                id=game_id,
                name=game_data['name'],
                jackpot=game_data['jackpot'],
                ticket_price=game_data['ticket_price'],
                draw_days=', '.join(game_data['draw_days']),
                next_draw=game_data['next_draw'],
                main_numbers_count=game_data['main_numbers_count'],
                main_numbers_range_low=game_data['main_numbers_range'][0],
                main_numbers_range_high=game_data['main_numbers_range'][1],
                special_ball_range_low=game_data.get('powerball_range', [None, None])[0] or game_data.get('mega_ball_range', [None, None])[0] or game_data.get('mega_number_range', [None, None])[0],
                special_ball_range_high=game_data.get('powerball_range', [None, None])[1] or game_data.get('mega_ball_range', [None, None])[1] or game_data.get('mega_number_range', [None, None])[1],
                special_ball_name= 'Powerball' if 'powerball_range' in game_data else 'Mega Ball' if 'mega_ball_range' in game_data else 'Mega Number' if 'mega_number_range' in game_data else None
            )
            db.session.add(new_game)

        db.session.commit()
    click.echo("Seeded the database with initial data.")


# Helper functions
def is_logged_in():
    """Check if user is logged in"""
    return 'user_id' in session

def get_current_user():
    """Get current logged in user data from database"""
    if is_logged_in():
        return db.session.get(User, session['user_id'])
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
    
    # Get featured games from DB
    featured_games = Game.query.filter(Game.id.in_(['mega_millions', 'powerball', 'superlotto_plus'])).all()
    
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
        user = User.query.filter_by(email=email).first()
        if user and user.password == password: # Insecure password check for prototype
            session['user_id'] = user.id
            session['user_email'] = user.email
            flash(f'Welcome back, {user.name}!', 'success')
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
    
    # Get all games from DB
    all_games = Game.query.order_by(Game.ticket_price.desc()).all()

    return render_template('dashboard.html', user=user, games=all_games)


@app.route('/account')
def account():
    """User account page, redirects to my_tickets for now"""
    login_check = require_login()
    if login_check:
        return login_check
    user = get_current_user()
    # Simple account page for now, can be expanded later
    return render_template('account.html', user=user)


@app.route('/my_tickets')
def my_tickets():
    """Displays user's active and past tickets."""
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()
    
    # Get tickets from DB, making sure to load the associated game data 
    # to avoid extra queries in the template (lazy loading).
    user_tickets = Ticket.query.filter_by(user_id=user.id).options(db.joinedload(Ticket.game)).order_by(Ticket.purchase_date.desc()).all()

    return render_template('my_tickets.html', user=user, tickets=user_tickets)


# Game and Shopping Routes
@app.route('/play/<game_id>')
def number_selection(game_id):
    """Page for selecting lottery numbers for a specific game."""
    login_check = require_login()
    if login_check:
        return login_check
        
    user = get_current_user()
    game = db.session.get(Game, game_id)

    if not game:
        flash('The requested game does not exist.', 'error')
        return redirect(url_for('dashboard'))

    # Get user's favorite numbers for this game
    favorite_numbers = FavoriteNumber.query.filter_by(user_id=user.id, game_id=game.id).all()

    return render_template('number_selection.html', user=user, game=game, favorites=favorite_numbers)

@app.route('/cart')
def cart():
    """Shopping cart view"""
    login_check = require_login()
    if login_check:
        return login_check
        
    user = get_current_user()
    
    # In this prototype, the cart is stored in the session
    cart_items = session.get('cart', [])
    
    # Calculate total
    total_price = sum(item['price'] for item in cart_items)

    return render_template('cart.html', user=user, cart_items=cart_items, total_price=total_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add selected numbers to cart"""
    login_check = require_login()
    if login_check:
        return login_check

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

@app.route('/remove_from_cart/<int:item_index>', methods=['POST'])
def remove_from_cart(item_index):
    """Remove an item from the cart"""
    login_check = require_login()
    if login_check:
        return login_check

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
    service_fee = subtotal * SERVICE_FEE_PERCENTAGE
    processing_fee = PROCESSING_FEE
    total = subtotal + service_fee + processing_fee
    
    # Check if user needs identity verification
    needs_verification = not user.is_identity_verified
    
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

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback() # Rollback the session in case of a DB error
    return render_template('500.html'), 500

# Development server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
