# Smart Task Manager

A Django-based task management application built for learning modern Python and Django development practices. This project serves as a hands-on learning experience for various Python/Django technologies and best practices.

## Learning Objectives

This project was built to gain practical experience with:

- **Django Web Framework**
  - Class-based views and function-based views
  - Custom user authentication
  - Django forms and model forms
  - URL routing and namespacing
  - Template inheritance
  - Django ORM and database migrations
  - Django admin customization

- **Advanced Django Features**
  - Custom user models
  - Django REST Framework for API development
  - Asynchronous task processing with Celery
  - Task scheduling with django-celery-beat
  - Redis as message broker and result backend
  - Django signals for event handling

- **Testing Best Practices**
  - pytest for testing
  - Fixtures and factory patterns
  - Test client and API client
  - Mock objects and test isolation
  - Coverage reporting

- **Modern Python Development**
  - Type hints and annotations
  - Async/await syntax
  - Python packaging
  - Environment management
  - Code organization and project structure

## Tech Stack

- **Backend Framework**: Django 5.2
- **Database**: PostgreSQL
- **Task Queue**: Celery
- **Message Broker**: Redis
- **API Framework**: Django REST Framework
- **Testing**: pytest, django-pytest
- **Task Scheduling**: django-celery-beat

## Features

- User authentication and authorization
- Project and task management
- Task assignments and tracking
- Email notifications
- Analytics and reporting
- RESTful API endpoints
- Scheduled tasks and background processing
- Export functionality

## Project Structure

```
smart_task_manager/
├── analytics/        # Analytics app for reporting
├── exports/         # Export functionality
├── notifications/   # Email notifications
├── tasks/          # Core task management
├── users/          # Custom user management
├── web/            # Web interface
└── smart_task_manager/  # Project settings
```

## Development Setup

1. Clone the repository
```bash
git clone <repository-url>
cd smart_task_manager
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations
```bash
python manage.py migrate
```

6. Start development server
```bash
python manage.py runserver
```

7. Start Celery worker and beat
```bash
celery -A smart_task_manager worker -l info
celery -A smart_task_manager beat -l info
```

## Testing

Run the test suite:
```bash
pytest
```

Generate coverage report:
```bash
pytest --cov
```

## Learning Resources

This project implements concepts from:
- Django Documentation
- Django REST Framework Tutorial
- Celery Best Practices
- Python Testing with pytest
- Modern Python Development Guides

## Future Learning Goals

- Docker containerization
- CI/CD pipelines
- AWS deployment
- Performance optimization
- Security best practices
- Frontend frameworks (React/Vue)

## License

This project is open-source and available under the MIT License.
