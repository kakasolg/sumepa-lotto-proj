Development Plan: Project LottoGo (Rapid Prototype)
Version: 1.2

Date: June 19, 2025

1. Executive Summary
Project LottoGo aims to develop a high-fidelity, functional prototype of a mobile-first lottery courier service. This service will allow users in California to securely order official state lottery tickets via a streamlined digital platform.

The primary objective of this prototype is to demonstrate a viable, user-centric, and legally compliant business model to secure seed funding. The prototype will showcase the complete end-to-end user journey, from initial discovery and onboarding to the ticket purchase and results management, with a strong emphasis on the compliance and payment mechanisms that navigate the industry's legal landscape.

This document outlines the project's core strategy, scope, key features, technology stack, and a high-level development timeline.

2. Project Goals & Scope
2.1. Primary Goals

Demonstrate Business Viability: Create a tangible product that clearly illustrates the service's value proposition and revenue model.

Validate User Experience: Showcase a seamless, intuitive, and trustworthy user journey optimized for mobile devices.

Prove Legal Compliance: Simulate the key verification and payment workflows designed to adhere to state and federal regulations.

Secure Investment: Serve as the primary demonstration tool for conversations with potential investors.

2.2. Scope of Work

In Scope (Features to be built)

Out of Scope (For this prototype)

End-to-end user journey simulation

Real-money payment processing

User registration and login

Direct integration with official lottery systems

Core Games: Powerball, Mega Millions, CA SuperLotto Plus

All other lottery games or "Bundle" features

Number selection (Manual, Quick Pick, Simulated Favorites)

A fully functional "Favorites" management system (CRUD)

Shopping cart and dynamic checkout flow

Live customer support chat or complex account management

Simulated Age & Identity Verification (at first purchase)

Integration with a real identity verification API (e.g., IDology)

Simulated Wallet Funding (ACH-only model via PayPal/Bank)

Real-world wallet funding or bank transfers

Post-purchase ticket management and lifecycle (Active -> Result)

Detailed transaction history or winning analysis

3. Core Strategy & Philosophy
This prototype will be built upon three foundational principles:

3.1. Business Flow First
The technology and features are designed to serve a well-defined business process. Our priority is to demonstrate a compliant and sustainable operational flow, from user verification to revenue generation (via service and processing fees), ensuring the model is sound from a legal and business perspective before scaling.

3.2. Mobile-First Design
Acknowledging that the target demographic primarily uses mobile devices for transactional services, the entire user interface and experience will be designed for a mobile screen first, then adapted for desktop. This ensures optimal usability, accessibility, and convenience for the majority of users.

3.3. Minimalist & Rapid Prototyping
The goal is speed and clarity. We will employ a minimalist design aesthetic, focusing on an intuitive user flow rather than complex visual embellishments. By leveraging modern frameworks like Flask and Tailwind CSS, we can rapidly develop and deploy a functional prototype, allowing for quick iteration based on feedback.

4. Key Features & Screen Layouts
The prototype will simulate the complete user lifecycle, with detailed screen compositions as follows:

1. Pre-Login Experience (Landing Page)

Layout: A three-section, single-page layout to effectively communicate value and build trust.

Hero Section: An engaging headline ("Play the Lottery: Anywhere, Any Device, Any Time"), a clear call-to-action ("Claim Free Ticket"), and mock-ups of the app on mobile/desktop.

Value Proposition: Highlights three core benefits (e.g., "Easy," "Safe," "Fast") with brief, benefit-oriented descriptions.

Trust & Offerings: Displays dynamic-looking lottery cards for Powerball and Mega Millions with large jackpot numbers to create urgency and excitement. A legal disclaimer is included at the bottom.

Navigation: A simple top navigation bar with the company logo and a user icon linking to the login/sign-up page.

2. Post-Login Experience (Main Dashboard - "Play" Tab)

Layout: A two-column grid layout optimized for quick game discovery.

Header: A personalized greeting ("Hi, [User Name]") and a visible wallet balance (e.g., "$0.00").

Navigation: A primary bottom or top navigation bar with icons for "Play," "Tickets," "Offers," and "Account," with "Play" being the active tab.

Content: Dynamic cards for the three core games (Powerball, Mega Millions, SuperLotto Plus), each displaying the game name, estimated jackpot, and the next draw date. Each card features a prominent "Play Now" button. Ancillary promotional elements will be excluded to maintain focus.

3. Interactive Number Selection Screen

Layout: A modal or full-screen view focused entirely on the ticket selection task.

Components:

Selected Numbers Display: A visual representation of empty slots (e.g., 5 white circles, 1 red circle) that get filled as the user makes selections.

Action Buttons: "Let Mido Pick" for instant random number generation and a "Favorite Set" button to simulate loading a pre-saved number combination.

Number Grid: An interactive grid of numbers (e.g., 1-47 for main numbers, 1-27 for the special number) that responds to user clicks.

Call to Action: An "Add to Cart" button that is initially disabled and becomes active only after a valid set of numbers is selected.

4. The Compliant Checkout Funnel (Payment Screens)
A multi-step, simulated process designed to demonstrate legal compliance and a clear revenue model.

Screen 1: Cart Review: An itemized list of tickets grouped by game. It shows quantities, sub-totals, and a final "Checkout" button leading to the next step.

Screen 2: Order & Fee Review: A transparent breakdown of all costs: ticket subtotal, a calculated Service Fee (e.g., 20% of ticket cost), and a flat Processing Fee (e.g., $1.00). The Total Charge is clearly displayed.

Screen 3: First-Purchase Verification Gate: If it's the user's first purchase attempt, they are redirected here. It presents a screen to "Verify your age" with options to "Scan ID" or "Manually Enter Details," simulating a compliance check powered by a service like IDology.

Screen 4: Payment Method Simulation: Guides the user through an ACH-only funding flow, explicitly stating that credit/debit cards are not allowed. It simulates choosing a funding source (e.g., PayPal) and confirming the transaction, emphasizing the link to a bank account.

5. Ticket Lifecycle Management (The "Tickets" Tab)
This tab provides users with a clean, organized view of their purchased tickets by implementing a status-based lifecycle.

Layout: A list of tickets, separated into two clear sections: "Upcoming Draws" and "Past Results."

Active Status: Tickets for future draws appear in the "Upcoming Draws" section, showing the game, selected numbers, and draw date.

Checked Status: Once a draw date has passed, the ticket moves to "Past Results." Its status is updated to Checked, and the UI clearly indicates the outcome (e.g., "Congratulations! You won $5" in green, or "Not a Winner" in grey).

Archived Status: After a short period (e.g., 3-5 days), Checked tickets are automatically removed from view (status changed to Archived in the database). This keeps the user's view clean and focused on current and recent activity.

6. Account Screen (The "Account" Tab)

Layout: A simple list-based menu providing access to essential account functions.

Components (Prototype):

Personal Details: Displays the user's name and email.

Manage Wallet/Payment: A link that simulates navigating to a page for managing linked bank accounts or viewing wallet balance (non-functional).

Help/Support: A link to a static contact information page.

Logout: A clearly visible button to sign out of the application.

5. Technology Stack
To achieve our rapid prototyping goals, we have selected a lightweight and efficient technology stack:

Backend Framework: Python (Flask)

Frontend Styling: Tailwind CSS (via CDN)

Database: SQLite

Deployment: AWS EC2 (Free Tier)

6. High-Level Project Timeline (Estimated)
This project is planned as a focused, 4-week sprint.

Week 1: Foundation & Onboarding

Project setup, database schema design (including Ticket.status and User.is_identity_verified).

Implement User Registration, Login, and Landing Page.

Build the main Dashboard and Account screen layouts.

Week 2: Core Gameplay Loop

Develop the dynamic Number Selection page.

Implement the Shopping Cart logic using sessions.

Build the Cart and initial Order Review pages.

Week 3: The Compliance Funnel

Build the simulated Age & Identity Verification flow.

Implement the multi-step, simulated Wallet Funding process.

Create the final "purchase completion" logic.

Week 4: Final Polish & Deployment

Implement the Ticket Lifecycle Management system and the "Tickets" tab UI.

Conduct end-to-end testing and user flow refinement.

Deploy the finished prototype to the AWS EC2 server.

7. Technical Implementation & Key Logic
This section outlines the core technical architecture and provides key code snippets that will serve as the foundation for the prototype development.

7.1. Database Schema (Models)
We will use Flask-SQLAlchemy to define our models. The core models will be User and Ticket.

# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # This flag is critical for the "First-Purchase Verification Gate"
    is_identity_verified = db.Column(db.Boolean, default=False, nullable=False)
    tickets = db.relationship('Ticket', backref='owner', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_name = db.Column(db.String(50), nullable=False)
    numbers = db.Column(db.String(100), nullable=False) # e.g., "6,16,20,29,41,27"
    draw_date = db.Column(db.DateTime, nullable=False)
    # This status field drives the entire ticket lifecycle
    status = db.Column(db.String(20), default='active', nullable=False) # active, checked, archived
    winnings = db.Column(db.Integer, default=0)

7.2. Key Backend Logic Snippets (Flask)

Dashboard Data Simulation:
This logic in the main dashboard route provides dynamic, up-to-date information for the game cards, making the application feel live.

# app.py
from flask import render_template, redirect, url_for
# ... other imports
from datetime import date, timedelta

def get_next_draw_date(today, draw_weekdays):
    # Helper function to calculate the next draw date
    # (e.g., Powerball is Mon, Wed, Sat -> 0, 2, 5)
    days_ahead = -1
    for i in range(7):
        next_day = (today.weekday() + i) % 7
        if next_day in draw_weekdays:
            days_ahead = i
            break
    return today + timedelta(days=days_ahead)

@app.route('/dashboard')
@login_required
def dashboard():
    today = date.today() # 2025-06-19
    # Powerball: Mon, Wed, Sat. Next is Sat (June 21)
    # Mega Millions: Tue, Fri. Next is Fri (June 20)
    # SuperLotto Plus: Wed, Sat. Next is Sat (June 21)

    games_for_dashboard = [
        {
            'id': 'mega_millions', 'name': 'Mega Millions',
            'jackpot': '243,000,000',
            'draw_date': get_next_draw_date(today, [1, 4]) # Tue, Fri
        },
        {
            'id': 'powerball', 'name': 'Powerball',
            'jackpot': '65,000,000',
            'draw_date': get_next_draw_date(today, [0, 2, 5]) # Mon, Wed, Sat
        },
        {
            'id': 'superlotto_plus', 'name': 'SuperLotto Plus',
            'jackpot': '15,000,000',
            'draw_date': get_next_draw_date(today, [2, 5]) # Wed, Sat
        }
    ]
    # This simulation must run before rendering the "Tickets" tab
    simulate_ticket_lifecycle(current_user)

    return render_template('dashboard.html', games=games_for_dashboard)

Ticket Lifecycle Simulation:
This function, called when a user views their tickets, simulates the passage of time and updates ticket statuses, a core feature for managing the user's view.

# app.py
import random
from datetime import datetime, timedelta

def simulate_ticket_lifecycle(user):
    # Step 1: Check for active tickets whose draw date has passed
    active_tickets = Ticket.query.filter_by(owner=user, status='active').all()
    for ticket in active_tickets:
        if ticket.draw_date < datetime.utcnow():
            ticket.status = 'checked'
            # Simulate a win with a 20% chance for demo purposes
            if random.random() < 0.2:
                ticket.winnings = random.choice([2, 5, 10, 100])
            else:
                ticket.winnings = 0
            db.session.add(ticket)

    # Step 2: Archive old, checked tickets (e.g., older than 3 days)
    checked_tickets = Ticket.query.filter_by(owner=user, status='checked').all()
    for ticket in checked_tickets:
        if ticket.draw_date < datetime.utcnow() - timedelta(days=3):
            ticket.status = 'archived'
            db.session.add(ticket)

    db.session.commit()
    
    ## 8. Current Development Status (June 19, 2025)
    
    ### 8.1 Completed Components ✅
    
    **Backend Infrastructure:**
    - ✅ Flask application structure (app.py)
    - ✅ Mock data system (mockdata.py) with test users and game data
    - ✅ Session-based authentication system
    - ✅ Core routing and navigation logic
    - ✅ Shopping cart functionality using Flask sessions
    
    **Frontend Templates:**
    - ✅ Base template with Tailwind CSS integration
    - ✅ Landing page with hero section, features, games showcase, and footer
    - ✅ Login page with demo account credentials
    - ✅ Register page with prototype notice
    - ✅ Dashboard with mobile-first navigation and game selection
    
    **Design System:**
    - ✅ Consistent color palette (LottoGo Blue, Gold, Green, Red)
    - ✅ Mobile-first responsive design
    - ✅ Modern glassmorphism and gradient effects
    - ✅ Professional typography using Inter font
    - ✅ Accessible component design
    
    ### 8.2 Implementation Notes
    
    **Technology Stack Used:**
    - **Backend:** Python Flask 3.1.1
    - **Frontend:** Tailwind CSS (CDN), HTML5, Vanilla JavaScript
    - **Data Storage:** Session-based (no SQLite in prototype)
    - **Package Management:** uv
    - **Development Environment:** Windows with Git
    
    **Key Features Implemented:**
    1. **Mock Authentication:** Demo account (demo@lottogo.com / demo123)
    2. **Responsive Navigation:** Bottom nav for mobile, desktop tabs
    3. **Game Management:** Powerball, Mega Millions, SuperLotto Plus
    4. **Visual Polish:** Modern UI with hover effects and transitions
    5. **Legal Compliance:** Proper disclaimers and age verification notices
    
    ### 8.3 Next Development Tasks
    
    **Immediate Priority (Next Session):**
    - [ ] Number selection interface with interactive grid
    - [ ] Shopping cart and checkout flow
    - [ ] Tickets management interface
    - [ ] Account management page
    - [ ] Basic error handling pages (404, 500)
    
    **Technical Debt:**
    - [ ] Add proper form validation
    - [ ] Implement CSRF protection
    - [ ] Add loading states and animations
    - [ ] Mobile testing and optimization
    - [ ] Performance optimization
    
    ### 8.4 Demo Instructions
    
    **To run the prototype:**
    1. Navigate to project directory: `D:\dev\html-prj\sumepa-lotto-proj`
    2. Activate virtual environment (if using venv)
    3. Run: `flask run` or `python app.py`
    4. Access: `http://localhost:5000`
    5. Login with: `demo@lottogo.com` / `demo123`
    
    **Prototype demonstrates:**
    - Landing page marketing flow
    - User authentication
    - Game selection interface
    - Mobile-responsive design
    - Professional UI/UX design
    
    This prototype successfully validates the core user journey and demonstrates the business model for potential investors.