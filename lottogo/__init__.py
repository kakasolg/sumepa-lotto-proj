# lottogo/__init__.py

import os
import click
from flask import Flask, session, redirect, url_for, flash, render_template
from .models import db, User, Game, Ticket, FavoriteNumber

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, 
                instance_relative_config=True, 
                template_folder='templates', 
                static_folder='static')
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    app.config.from_mapping(
        SECRET_KEY='lottogo_dev_secret_key_2025', # Change this for production
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'lottogo.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

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
            from .mockdata import TEST_USERS, GAMES
            # Clear existing data
            db.session.query(FavoriteNumber).delete()
            db.session.query(Ticket).delete()
            db.session.query(User).delete()
            db.session.query(Game).delete()
            
            # Seed Users
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

    # Register Blueprints
    from .routes import main, auth, tickets
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(tickets.bp)

    # Make url_for('index') work for the main blueprint
    app.add_url_rule('/', endpoint='main.landing')

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback() # Rollback the session in case of a DB error
        return render_template('500.html'), 500
        
    return app
