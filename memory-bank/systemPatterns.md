# System Patterns: LottoGo

## Architecture Overview
**Type:** Monolithic Flask web application  
**Pattern:** MVC with session-based authentication  
**Deployment:** Single-instance prototype  

## Key Technical Decisions

### Backend Framework
- **Choice:** Python Flask 3.1.1
- **Rationale:** Rapid prototyping, simplicity, Python ecosystem
- **Benefits:** Quick development, minimal boilerplate, flexible routing

### Frontend Approach
- **Choice:** Server-side rendered templates with Tailwind CSS
- **Rationale:** Simplicity over complexity, rapid styling, responsive design
- **Benefits:** No build process, CDN delivery, mobile-first utilities

### Data Strategy
- **Current:** Session-based storage with mock data
- **Planned:** SQLite with SQLAlchemy ORM
- **Rationale:** Prototype speed now, easy migration later

### Authentication Pattern
- **Current:** Session-based with mock users
- **Pattern:** Flask session management
- **Security Note:** Demo-only, not production-ready

## Design Patterns in Use

### Template Inheritance
```
base.html (master layout)
├── landing.html (marketing page)
├── login.html (authentication)
├── register.html (registration)
└── dashboard.html (main app)
```

### Color System
- **Primary:** LottoGo Blue (#1e40af, #3b82f6)
- **Accent:** Gold (#f59e0b, #fbbf24)
- **Success:** Green (#10b981, #34d399)
- **Danger:** Red (#ef4444, #f87171)
- **Neutral:** Gray scale (#374151, #6b7280, #9ca3af)

### Component Patterns

#### Game Cards
- Consistent structure: game name, jackpot, draw date, CTA
- Hover effects and transitions
- Mobile-responsive grid layout

#### Navigation
- Bottom navigation for mobile
- Tab navigation for desktop
- Active state management

#### Form Patterns
- Consistent styling with Tailwind utilities
- Validation feedback preparation
- Accessible labeling

## Component Relationships

### Page Flow Architecture
```
Landing Page
├── Login → Dashboard
├── Register → Dashboard
└── Dashboard
    ├── Play Tab (active)
    ├── Tickets Tab (planned)
    ├── Offers Tab (planned)
    └── Account Tab (planned)
```

### Session Management
- User authentication state in Flask session
- Shopping cart data in session storage
- Navigation state preservation

### Mock Data Structure
```python
# mockdata.py structure
DEMO_USERS = {
    'demo@lottogo.com': {
        'password': 'demo123',
        'name': 'Demo User'
    }
}

GAMES = {
    'powerball': {...},
    'mega_millions': {...},
    'superlotto_plus': {...}
}
```

## Critical Implementation Paths

### Authentication Flow
1. Landing page → Login form
2. Credential validation against mock data
3. Session establishment
4. Redirect to dashboard
5. Session-protected routes

### Game Selection Flow
1. Dashboard display with dynamic game data
2. Game card interaction
3. Number selection interface (planned)
4. Shopping cart management (planned)
5. Checkout process (planned)

### Responsive Design Pattern
- Mobile-first CSS with min-width breakpoints
- Flexible grid systems using Tailwind
- Touch-friendly interactive elements
- Progressive enhancement for desktop

## Security Considerations (Prototype Level)
- Session-based authentication (demo only)
- CSRF protection (planned)
- Input validation (planned)
- Secure headers (planned)

## Performance Patterns
- CDN-delivered CSS (Tailwind via CDN)
- Minimal JavaScript dependencies
- Optimized image assets
- Session-based caching for user state

## Development Patterns
- Single-file Flask application for simplicity
- Template-based rendering
- Mock data separation for testing
- Git-based version control
- Package management via uv
