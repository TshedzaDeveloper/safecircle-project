# SafeCircle

SafeCircle is a Django-based web application designed to help communities report crimes, send emergency alerts, and view community safety information.

## Features

- Crime reporting with location tracking
- Emergency alert system
- Community safety groups (SafeCircles)
- Interactive map of reported incidents
- Anonymous reporting option
- Media upload support (photos/audio)
- Admin dashboard for community leaders

## Technology Stack

- Django 5.2
- Django REST Framework
- Bootstrap 5
- Leaflet.js for maps
- PostgreSQL (production)
- SQLite (development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TshedzaDeveloper/TshedzaWorksapce.git
cd TshedzaWorksapce/safecircle
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `core/` - Core functionality and user management
- `reports/` - Crime reporting and emergency alerts
- `safecircles/` - Community safety groups
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Diepsloot Community
- Local Law Enforcement
- Community Safety Organizations

## Target Users

- Community Members
- Local Authorities
- Safety Organizations
- Community Leaders 