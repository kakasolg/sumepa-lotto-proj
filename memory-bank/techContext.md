# Technical Context: LottoGo

## Technology Stack

### Backend
- **Framework:** Python Flask 3.1.1
- **Language:** Python 3.12+
- **Package Manager:** uv (ultra-fast Python package installer)
- **Database:** Session-based (SQLite planned)
- **ORM:** SQLAlchemy (planned implementation)

### Frontend
- **Styling:** Tailwind CSS 3.x (via CDN)
- **JavaScript:** Vanilla ES6+ (minimal usage)
- **Templates:** Jinja2 (Flask default)
- **Fonts:** Inter (Google Fonts)
- **Icons:** Custom styling (no icon library)

### Development Environment
- **OS:** Windows
- **Shell:** cmd.exe
- **Editor:** VS Code
- **Version Control:** Git
- **Virtual Environment:** .venv (Python venv)

### Deployment Target
- **Platform:** AWS EC2 Free Tier (planned)
- **Server:** Gunicorn (planned)
- **Reverse Proxy:** Nginx (planned)

## Development Setup

### Project Structure
```
sumepa-lotto-proj/
├── app.py              # Main Flask application
├── main.py             # Alternative entry point
├── mockdata.py         # Demo users and game data
├── pyproject.toml      # Project configuration
├── uv.lock            # Dependency lock file
├── static/            # CSS, JS, images
├── templates/         # Jinja2 templates
└── docs/             # Project documentation
```

### Virtual Environment
- **Created with:** `python -m venv .venv`
- **Activation:** `.venv\Scripts\activate` (Windows)
- **Package management:** uv for speed

### Running the Application
```cmd
# Development server
flask run
# OR
python app.py

# Access: http://localhost:5000
```

## Technical Constraints

### Prototype Limitations
- **No real database:** Session-based storage only
- **No real payments:** Simulated ACH/PayPal flow
- **No external APIs:** Mock data for all services
- **No production security:** Demo authentication only

### Legal/Compliance Constraints
- **Payment Methods:** ACH-only (no credit/debit cards)
- **Age Verification:** Required simulation on first purchase
- **State Limitation:** California only
- **Lottery Games:** Only Powerball, Mega Millions, SuperLotto Plus

### Performance Constraints
- **Single-threaded:** Flask development server
- **Session storage:** Memory-based, not persistent
- **No caching:** Direct template rendering
- **No CDN:** Local static file serving

## Dependencies

### Core Dependencies (pyproject.toml)
```toml
[project]
dependencies = [
    "flask>=3.1.1",
    "flask-sqlalchemy",  # For future database integration
]
```

### Frontend Dependencies
- **Tailwind CSS:** `https://cdn.tailwindcss.com`
- **Inter Font:** Google Fonts CDN
- **No JavaScript frameworks:** Vanilla JS only

## Tool Usage Patterns

### Package Management with uv
```cmd
# Install dependencies
uv pip install flask

# Add new dependency
uv add package-name

# Update lock file
uv lock
```

### Development Workflow
1. **Code changes:** Edit Flask app or templates
2. **Hot reload:** Flask development server auto-reloads
3. **Testing:** Manual browser testing
4. **Version control:** Git commits for progress tracking

### File Organization
- **Static assets:** `/static/css/`, `/static/js/`, `/static/images/`
- **Templates:** `/templates/` with base template inheritance
- **Configuration:** Environment variables (planned)
- **Documentation:** `/docs/` markdown files

## Integration Points

### Mock Data Integration
- **Users:** `mockdata.py` contains demo credentials
- **Games:** Dynamic jackpot and draw date simulation
- **Session management:** Flask session for user state

### Planned Integrations
- **Database:** SQLite with SQLAlchemy models
- **Payment:** PayPal API simulation
- **Identity verification:** IDology API simulation
- **Lottery APIs:** State lottery system simulation

## Security Configuration

### Current (Prototype)
- **Session secret:** Hardcoded (not production-ready)
- **Authentication:** Simple password check
- **HTTPS:** Not implemented (local development)

### Planned (Production)
- **Environment variables:** Secret key management
- **CSRF protection:** Flask-WTF integration
- **Secure headers:** Security middleware
- **HTTPS:** SSL certificate configuration

## Performance Considerations

### Current Optimizations
- **CDN delivery:** Tailwind CSS from CDN
- **Minimal JavaScript:** Reduced client-side processing
- **Template caching:** Jinja2 built-in caching

### Planned Optimizations
- **Database indexing:** SQLite query optimization
- **Static file caching:** Nginx static file serving
- **Compression:** Gzip response compression
- **Minification:** CSS/JS asset optimization
