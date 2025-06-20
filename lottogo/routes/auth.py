# lottogo/routes/auth.py

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import functools

from ..models import db, User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        flash('Registration is not available in this prototype. Use demo@lottogo.com / demo123', 'info')
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if g.user:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Invalid email or password.'
        # Insecure password check for prototype
        elif user.password != password: 
            error = 'Invalid email or password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('main.dashboard'))

        flash(error, 'error')

    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    """If a user id is in the session, load the user object from
    the database and make it available in g.user."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)

@bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.landing'))

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
