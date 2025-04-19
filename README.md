# Smart Task Manager

A modern task management application built with Django.

## Tech Stack

### Backend
- **Python 3.x**: Core programming language
- **Django**: Web framework
- **Django REST Framework**: For building RESTful APIs
- **PostgreSQL**: Database for both development and production environments

### Testing
- **pytest**: Python testing framework
- **pytest-django**: Django plugin for pytest
- **pytest-cov**: For test coverage reporting

### Development Tools
- **Black**: Code formatting
- **Flake8**: Code linting
- **isort**: Import sorting

## Testing

This project uses pytest for testing. To run the tests:

```bash
# Install test dependencies
pip install pytest pytest-django pytest-cov

# Run tests
pytest

# Run tests with coverage report
pytest --cov=smart_task_manager
```

## Getting Started

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
smart_task_manager/
├── manage.py
├── smart_task_manager/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── README.md
```

## Contributing

1. Create a new branch for your feature
2. Write tests for new functionality
3. Ensure all tests pass
4. Submit a pull request

## License

This project is licensed under the MIT License.
