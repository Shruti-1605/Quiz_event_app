# Quiz & Events Platform

A Django-based interactive quiz and events platform with modern UI design.

## Features
- Interactive quizzes with multiple programming languages
- User authentication and registration
- Personal quiz attempt tracking
- Events management
- Admin dashboard for content management
- Responsive design with TailwindCSS

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Quiz_Events_Project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install django
pip install djangorestframework
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Username: shruti
# Password: MYPass@2025
```

### 6. Add Sample Data
After creating superuser, login to admin panel at `http://127.0.0.1:8000/admin/` and add:
- Quizzes with questions and answers
- Events
- Categories

### 7. Run Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the platform.

## Admin Access
- Only superuser with username "shruti" has full admin access
- Admin panel: `http://127.0.0.1:8000/admin/`
- Admin buttons appear on home page for authorized users

## Project Structure
```
Quiz_Events_Project/
├── quiz_events_app/
│   ├── models.py          # Database models
│   ├── views.py           # Web views
│   ├── api_views.py       # API endpoints
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # URL routing
│   └── templates/         # HTML templates
├── quiz_events_project/
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL config
└── manage.py              # Django management
```

## Technologies Used
- Django 5.2.7
- Django REST Framework
- TailwindCSS
- Font Awesome Icons
- SQLite Database

