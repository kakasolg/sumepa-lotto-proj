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


@app.route('/account', methods=['GET', 'POST'])
def account():
    """User account page, allows updating password."""
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not new_password or new_password != confirm_password:
            flash('Passwords do not match or are empty.', 'error')
            return redirect(url_for('account'))

        # In a real app, you should hash the password.
        # For this prototype, we'll store it as plain text.
        user.password = new_password
        db.session.commit()

        flash('Your password has been updated successfully.', 'success')
        return redirect(url_for('account'))

    # For GET request, just render the page
    return render_template('account.html', user=user)


@app.route('/my_tickets')
def my_tickets():
    """Displays user's active and past tickets."""
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()
    
    # Calculate the cutoff date: 3 days ago from today
    cutoff_date = datetime.utcnow() - timedelta(days=3)

    # Get tickets from DB, filtering out any tickets whose draw date is older than the cutoff
    user_tickets = Ticket.query.filter_by(user_id=user.id)\
                                .filter(Ticket.draw_date >= cutoff_date)\
                                .options(db.joinedload(Ticket.game))\
                                .order_by(Ticket.purchase_date.desc()).all()

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
        flash('Game not found!', 'error')
        return redirect(url_for('dashboard'))

    return render_template('number_selection.html', user=user, game=game)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    login_check = require_login()
    if login_check:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request'}), 400

    game_id = data.get('game_id')
    tickets_data = data.get('tickets')
    user = get_current_user()
    game = db.session.get(Game, game_id)

    if not game or not tickets_data:
        return jsonify({'success': False, 'message': 'Invalid game or ticket data'}), 400

    if 'cart' not in session:
        session['cart'] = []

    for ticket_data in tickets_data:
        special_ball_field = game.special_ball_name.lower().replace(' ', '_') if game.special_ball_name else None
        
        new_ticket_for_cart = {
            'game_id': game.id,
            'game_name': game.name,
            'ticket_price': game.ticket_price,
            'main_numbers': ticket_data.get('numbers'),
            'special_number': ticket_data.get(special_ball_field) if special_ball_field else None
        }
        session['cart'].append(new_ticket_for_cart)

    session.modified = True

    return jsonify({'success': True, 'cart_count': len(session['cart'])})


@app.route('/cart')
def cart():
    login_check = require_login()
    if login_check:
        return login_check
    
    user = get_current_user()
    cart_items = session.get('cart', [])
    
    total_price = sum(item['ticket_price'] for item in cart_items)

    return render_template('cart.html', user=user, cart_items=cart_items, total_price=total_price)


@app.route('/remove_from_cart/<int:item_index>')
def remove_from_cart(item_index):
    login_check = require_login()
    if login_check:
        return login_check

    if 'cart' in session and len(session['cart']) > item_index:
        session['cart'].pop(item_index)
        session.modified = True
        flash('Item removed from your cart.', 'success')
    else:
        flash('Item not found in your cart.', 'error')

    return redirect(url_for('cart'))


@app.route('/clear_cart')
def clear_cart():
    login_check = require_login()
    if login_check:
        return login_check

    if 'cart' in session:
        session.pop('cart', None)
        flash('Your cart has been cleared.', 'success')

    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    login_check = require_login()
    if login_check:
        return login_check

    user = get_current_user()
    cart_items = session.get('cart', [])

    if not cart_items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('dashboard'))

    total_price = sum(item['ticket_price'] for item in cart_items)

    if request.method == 'POST':
        # The form submission now leads to the verification flow
        # The actual purchase logic will be handled later
        
        # Store cart and total price in session to retrieve later
        session['purchase_context'] = {
            'cart': cart_items,
            'total_price': total_price
        }
        session.modified = True

        if user.wallet_balance >= total_price:
            # If balance is sufficient, proceed to identity verification
            return redirect(url_for('verify_age'))
        else:
            # If balance is insufficient, redirect to add funds
            flash('You have insufficient funds. Please add funds to your wallet.', 'warning')
            return redirect(url_for('load_options'))

    return render_template('checkout.html', user=user, cart_items=cart_items, total_price=total_price)


# --- Verification and Purchase Flow ---
@app.route('/verify_age', methods=['GET'])
def verify_age():
    login_check = require_login()
    if login_check: return login_check
    return render_template('verify_age.html', user=get_current_user())

@app.route('/verify_manual', methods=['GET', 'POST'])
def verify_manual():
    login_check = require_login()
    if login_check: return login_check

    if request.method == 'POST':
        # In a real app, this data would be sent to an identity provider.
        # For this demo, we just check if fields are filled and move on.
        full_name = request.form.get('full_name')
        dob = request.form.get('dob')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')

        if not all([full_name, dob, address, city, state, zip_code]):
            flash('Please fill out all required fields.', 'error')
            return redirect(url_for('verify_manual'))
        
        # Mark verification as passed in session and proceed
        session['identity_verified_for_purchase'] = True
        session.modified = True
        
        # After verification, check wallet balance again before proceeding
        user = get_current_user()
        purchase_context = session.get('purchase_context', {})
        total_price = purchase_context.get('total_price', 0)

        if user.wallet_balance >= total_price:
             # If funds are sufficient, go to the confirmation page
            return redirect(url_for('confirm_purchase'))
        else:
            # If funds are insufficient, go to payment options
            flash('Identity verified, but your wallet balance is too low.', 'warning')
            return redirect(url_for('load_options'))

    return render_template('verify_manual.html', user=get_current_user())

@app.route('/confirm_purchase', methods=['GET'])
def confirm_purchase():
    login_check = require_login()
    if login_check: return login_check

    # Ensure user has verified their identity for this purchase
    if not session.get('identity_verified_for_purchase'):
        flash('Please verify your identity first.', 'error')
        return redirect(url_for('verify_age'))

    # Ensure there is a purchase context
    if 'purchase_context' not in session:
        flash('Your session has expired. Please start over.', 'error')
        return redirect(url_for('cart'))

    return render_template('confirm_purchase.html', user=get_current_user(), session=session)


@app.route('/load_options', methods=['GET'])
def load_options():
    login_check = require_login()
    if login_check: return login_check
    # User might land here without having verified identity if funds were insufficient from checkout
    # if not session.get('identity_verified_for_purchase'):
    #     return redirect(url_for('verify_age'))
    
    purchase_context = session.get('purchase_context', {})
    
    return render_template('load_options.html', user=get_current_user(), session=session)

@app.route('/paypal_info', methods=['GET'])
def paypal_info():
    login_check = require_login()
    if login_check: return login_check
    # Allow access even if not verified, as they might be funding account first
    # if not session.get('identity_verified_for_purchase'):
    #     return redirect(url_for('verify_age'))
    return render_template('paypal_info.html', user=get_current_user(), session=session)


@app.route('/finalize_purchase', methods=['POST'])
def finalize_purchase():
    login_check = require_login()
    if login_check: return login_check

    user = get_current_user()
    purchase_context = session.get('purchase_context')

    # Security check: Ensure user has gone through the necessary steps
    if not purchase_context or not session.get('identity_verified_for_purchase'):
        flash('Your session is invalid or has expired. Please try again.', 'error')
        return redirect(url_for('dashboard'))

    # This is a simulation. If the user came from the payment flow,
    # we pretend they topped up their wallet.
    # We add the required amount to their balance before proceeding.
    total_price = purchase_context['total_price']
    if user.wallet_balance < total_price:
        amount_to_add = total_price - user.wallet_balance
        user.wallet_balance += amount_to_add
        db.session.commit()
        flash(f'Successfully added ${amount_to_add:.2f} to your wallet.', 'success')


    # Now, perform the final check and purchase logic
    if user.wallet_balance >= total_price:
        user.wallet_balance -= total_price
        for item in purchase_context['cart']:
            game = db.session.get(Game, item['game_id'])
            if not game:
                continue # Or handle error appropriately

            # Parse draw date from string, with a fallback
            try:
                draw_date = datetime.strptime(game.next_draw.split('.')[0], '%Y-%m-%d %H:%M:%S')
            except (ValueError, AttributeError):
                draw_date = datetime.utcnow() + timedelta(days=3) # Fallback

            new_ticket = Ticket(
                id=f"TICKET-{user.id}-{int(datetime.utcnow().timestamp())}-{random.randint(1000, 9999)}",
                user_id=user.id,
                game_id=item['game_id'],
                purchase_date=datetime.utcnow(),
                draw_date=draw_date,
                numbers=",".join(map(str, item['main_numbers'])),
                special_ball=str(item['special_number']) if item['special_number'] is not None else None,
                status='active',
                winnings=0.0
            )
            db.session.add(new_ticket)
        
        db.session.commit()

        # Clear session data related to the purchase
        session.pop('cart', None)
        session.pop('purchase_context', None)
        session.pop('identity_verified_for_purchase', None)
        session.modified = True

        flash('Your purchase was successful! Good luck!', 'success')
        return redirect(url_for('my_tickets'))
    else:
        flash('An error occurred with your wallet balance.', 'error')
        return redirect(url_for('checkout'))

# --- Purchase Flow Success --- 
@app.route('/purchase_success')
def purchase_success():
    login_check = require_login()
    if login_check: return login_check
    return render_template('purchase_success.html')


# --- Admin Management Routes ---
@app.route('/adminmanage')
def admin_manage():
    # A simple, unprotected admin page for demo purposes.
    all_users = User.query.all()
    all_tickets = Ticket.query.order_by(Ticket.purchase_date.desc()).all()
    return render_template('admin_manage.html', all_users=all_users, all_tickets=all_tickets, is_admin_view=True)

@app.route('/admin/add_funds/<int:user_id>', methods=['POST'])
def admin_add_funds(user_id):
    user = db.session.get(User, user_id)
    if user:
        try:
            amount = float(request.form.get('amount'))
            user.wallet_balance += amount
            db.session.commit()
            flash(f'Successfully added ${amount:.2f} to {user.name}\'s wallet.', 'success')
        except (ValueError, TypeError):
            flash('Invalid amount entered.', 'error')
    else:
        flash('User not found.', 'error')
    return redirect(url_for('admin_manage'))

@app.route('/admin/delete_ticket/<ticket_id>', methods=['POST'])
def admin_delete_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)
    if ticket:
        db.session.delete(ticket)
        db.session.commit()
        flash(f'Ticket {ticket_id} has been deleted successfully.', 'success')
    else:
        flash('Ticket not found.', 'error')
    return redirect(url_for('admin_manage'))


@app.route('/admin/update_password/<int:user_id>', methods=['POST'])
def admin_update_password(user_id):
    user = db.session.get(User, user_id)
    if user:
        new_password = request.form.get('new_password')
        if new_password and len(new_password) >= 4:
            user.password = new_password # In a real app, hash this
            db.session.commit()
            flash(f'Successfully updated password for {user.name}.', 'success')
        else:
            flash('Password must be at least 4 characters long.', 'error')
    else:
        flash('User not found.', 'error')
    return redirect(url_for('admin_manage'))


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
