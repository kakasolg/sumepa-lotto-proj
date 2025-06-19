# Mock data for LottoGo prototype
# This will be replaced with actual database queries in production

from datetime import datetime, timedelta
import random

# Test users for development
TEST_USERS = {
    'demo@lottogo.com': {
        'id': 1,
        'email': 'demo@lottogo.com',
        'name': 'Demo User',
        'phone': '+1-555-0123',
        'password': 'demo123',
        'is_identity_verified': True,
        'wallet_balance': 25.00
    },
    'john@example.com': {
        'id': 2,
        'email': 'john@example.com', 
        'name': 'John Smith',
        'phone': '+1-555-0456',
        'password': 'test123',
        'is_identity_verified': False,
        'wallet_balance': 0.00
    }
}

# Mock game data
GAMES = {
    'powerball': {
        'id': 'powerball',
        'name': 'Powerball',
        'jackpot': '$65,000,000',
        'ticket_price': 2.00,
        'draw_days': ['Monday', 'Wednesday', 'Saturday'],
        'next_draw': 'Saturday, June 21, 2025',
        'main_numbers_count': 5,
        'main_numbers_range': (1, 69),
        'powerball_range': (1, 26)
    },
    'mega_millions': {
        'id': 'mega_millions',
        'name': 'Mega Millions',
        'jackpot': '$243,000,000',
        'ticket_price': 2.00,
        'draw_days': ['Tuesday', 'Friday'],
        'next_draw': 'Friday, June 20, 2025',
        'main_numbers_count': 5,
        'main_numbers_range': (1, 70),
        'mega_ball_range': (1, 25)
    },
    'superlotto_plus': {
        'id': 'superlotto_plus',
        'name': 'SuperLotto Plus',
        'jackpot': '$15,000,000',
        'ticket_price': 1.00,
        'draw_days': ['Wednesday', 'Saturday'],
        'next_draw': 'Saturday, June 21, 2025',
        'main_numbers_count': 5,
        'main_numbers_range': (1, 47),
        'mega_number_range': (1, 27)
    }


# Mock ticket data - will be stored in session in this prototype
# In production, this would be in the database
MOCK_TICKETS = [
    {
        'id': 'T001',
        'user_id': 1,
        'game': 'powerball',
        'numbers': '07, 10, 25, 32, 44',
        'powerball': '18',
        'draw_date': datetime.now() + timedelta(days=2),
        'status': 'active',
        'purchase_date': datetime.now() - timedelta(days=1),
        'winnings': 0
    },
    {
        'id': 'T002', 
        'user_id': 1,
        'game': 'mega_millions',
        'numbers': '12, 29, 30, 33, 61',
        'mega_ball': '18',
        'draw_date': datetime.now() - timedelta(days=3),
        'status': 'checked',
        'purchase_date': datetime.now() - timedelta(days=5),
        'winnings': 5
    },
    {
        'id': 'T003',
        'user_id': 1,
        'game': 'superlotto_plus',
        'numbers': '05, 14, 22, 30, 41',
        'mega_number': '12',
        'draw_date': datetime.now() - timedelta(days=10),
        'status': 'archived',  # Will be hidden from user view
        'purchase_date': datetime.now() - timedelta(days=12),
        'winnings': 0
    }
]

# Mock favorite number sets
FAVORITE_NUMBERS = {
    1: [  # user_id 1
        {
            'id': 'F001',
            'name': 'Lucky Numbers',
            'game': 'powerball',
            'numbers': '07, 10, 25, 32, 44',
            'powerball': '18'
        },
        {
            'id': 'F002',
            'name': 'Birthday Set',
            'game': 'mega_millions',
            'numbers': '05, 12, 18, 25, 31',
            'mega_ball': '07'
        }
    ]


# Service fees configuration
SERVICE_FEES = {
    'service_fee_percentage': 0.20,  # 20% of ticket cost
    'processing_fee': 1.00           # Flat $1.00 processing fee
}

# Utility functions for mock data
def get_user_by_email(email):
    """Get user data by email (simulates database query)"""
    return TEST_USERS.get(email)

def get_user_tickets(user_id, status=None):
    """Get user tickets by status (simulates database query)"""
    tickets = [t for t in MOCK_TICKETS if t['user_id'] == user_id]
    if status:
        tickets = [t for t in tickets if t['status'] == status]
    return tickets

def get_user_favorites(user_id):
    """Get user favorite number sets (simulates database query)"""
    return FAVORITE_NUMBERS.get(user_id, [])

def simulate_ticket_lifecycle():
    """Simulate ticket status changes based on draw dates"""
    # TODO: In production, this would be a scheduled job
    # that checks draw dates and updates ticket statuses
    for ticket in MOCK_TICKETS:
        if ticket['status'] == 'active' and ticket['draw_date'] < datetime.now():
            ticket['status'] = 'checked'
            # Simulate random winnings
            if random.random() < 0.15:  # 15% chance to win something
                ticket['winnings'] = random.choice([2, 5, 10, 100])
        
        # Archive tickets older than 7 days after draw
        if (ticket['status'] == 'checked' and 
            ticket['draw_date'] < datetime.now() - timedelta(days=7)):
            ticket['status'] = 'archived'