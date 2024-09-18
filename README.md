# Ad System

This project implements a system where users can post Ads and comment on other users' Ads. Users need to be authenticated for actions like posting Ads or commenting, but they can view Ads and comments without being logged in. This is a RESTful API built with Django REST Framework and uses PostgreSQL as the database.

## Features

- **User Authentication**: Users can register and log in using an email (as username) and password.
- **Ad Management**: Authenticated users can create, edit, and delete their own Ads.
- **Commenting System**: Authenticated users can comment on others' Ads but only once per Ad.
- **Public Access**: Ads and related comments can be viewed without authentication.
- **Pagination**: Ads and comments are paginated for better performance.
- **API Documentation**: OpenAPI specification available for easy exploration of API endpoints.

## Tech Stack

- **Django**: Python-based web framework.
- **Django REST Framework**: Toolkit for building Web APIs.
- **PostgreSQL**: Relational database used for storage.
- **drf-spectacular**: OpenAPI/Swagger documentation generation for DRF.

## Requirements

- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ZahraMatinfar/2FCJ3-23459.git
```

### 2. Create a virtual environment and activate it


```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL
- Make sure PostgreSQL is installed and running.
Create a database for the project:

    ``` bash
    -> psql
    CREATE DATABASE [db_name];
    ```

- Create a .ven file (There is a .env.example. You can use as the reference)


### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

## Running Tests
The project includes tests for the API endpoints. You can run the tests using the following command:

```bash
python manage.py test
```

## OpenAPI/Swagger Documentation
You can explore the API interactively using Swagger. Access the API documentation at:

Schema: http://127.0.0.1:8000/api/schema/
Doc: http://127.0.0.1:8000/api/docs/

## Pagination
Both Ads and Comments use pagination. By default, the page size is set to 10. You can use the page query parameter to navigate between pages:

``` bash
GET /ads/?page=2
GET /ads/{ad_id}/comments/?page=1
```
