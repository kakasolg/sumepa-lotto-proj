# lottogo/routes/main.py

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import random
from ..models import db, User, Game, Ticket, FavoriteNumber
from .auth import login_required

bp = Blueprint('main', __name__)

def is_logged_in():
    return 'user_id' in session

def get_current_user():
    if is_logged_in():
        return db.session.get(User, session['user_id'])
    return None

@bp.route('/')
def landing():
    """Landing page for non-logged in users"""
    if g.user:
        return redirect(url_for('main.dashboard'))
    
    featured_games = Game.query.filter(Game.id.in_(['mega_millions', 'powerball', 'superlotto_plus'])).all()
    
    return render_template('landing.html', games=featured_games)

@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - Play tab"""
    all_games = Game.query.order_by(Game.ticket_price.desc()).all()
    return render_template('dashboard.html', user=g.user, games=all_games)

@bp.route('/account')
@login_required
def account():
    """User account page"""
    return render_template('account.html', user=g.user)

@bp.route('/my_tickets')
@login_required
def my_tickets():
    """Displays user's active and past tickets."""
    user_tickets = Ticket.query.filter_by(user_id=g.user.id).options(db.joinedload(Ticket.game)).order_by(Ticket.purchase_date.desc()).all()

    return render_template('my_tickets.html', user=g.user, tickets=user_tickets)
