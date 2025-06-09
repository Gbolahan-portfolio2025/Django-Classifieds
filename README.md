# Django Classifieds

A multi-user classifieds site built with Django and PostgreSQL.

## Features

- User registration and authentication
- Create, edit, and delete classified ads
- Permissions to restrict ad editing to owners only
- Pagination for ads listing
- PostgreSQL as database backend

## Setup

1. Create and activate your virtual environment
2. Install requirements: `pip install -r requirements.txt`
3. Set up your `.env` file with database credentials
4. Run migrations: `python manage.py migrate`
5. Run the development server: `python manage.py runserver`
