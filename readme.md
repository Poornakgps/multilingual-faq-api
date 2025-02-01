# Multilingual FAQ API

This project implements a **RESTful API** for managing Frequently Asked Questions (**FAQs**) with support for multiple languages using **Django** and **Django REST Framework**.

## Features
- **CRUD Operations**: Create, read, update, and delete FAQs.
- **Automatic Translation**: Supports multiple languages (**Hindi, Bengali, Telugu, Tamil, Malayalam, Kannada**).
- **Language-Specific Retrieval**: Fetch FAQs in a specific language.
- **Caching with Redis**: Improves performance using **Redis** for caching.
- **WYSIWYG Editor**: Uses **CKEditor** for rich text answers.
- **Docker Support**: Run the application using **Docker**.

## Prerequisites
Ensure you have the following installed:
- **Python 3.10+**
- **pip** (Python package manager)
- **virtualenv**
- **Redis**
- **Docker**

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Poornakgps/multilingual-faq-api.git
cd multilingual-faq-api
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Redis and Database
```bash
sudo apt-get install redis-server
sudo service redis-server start
```

### 5. Make Migrations
```bash
python manage.py makemigrations faq
```

### 6. Apply Migrations
```bash
python manage.py migrate
```

### 7. Create a Superuser (Admin Access)
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

### 9. Run the Redis Server
```bash
redis-server
```

### 10. Run The Test Cases
```bash
python manage.py test
```

Your API is now running at **http://127.0.0.1:8000/** 🚀

## Running with Docker
If you prefer running the application using **Docker**, follow these steps:

### 1. Build the Docker Image
```bash
docker build -t multilingual-faq-api .
```

### 2. Run the Docker Container
```bash
docker run -p 8000:8000 multilingual-faq-api
```

Your API will be accessible at **http://localhost:8000/**.

## API Endpoints

Replace `<int:id>` with id and `<str:lang>` with language.

| Method | Endpoint | Description |
|--------|-----------------------------|---------------------------------------------|
| **POST** | `/api/faq/create/` | Create a new FAQ | // done |
| **GET** | `/api/faq/` | Retrieve all FAQs | // done |
| **GET** | `/api/faq/language/<str:lang>/` | Retrieve FAQs in a specific language | // done |
| **GET** | `/api/faq/<int:id>/language/<str:lang>/` | Retrieve a single FAQ by ID | // done |
| **PUT** | `/api/faq/<int:id>/update/` | Update an FAQ by ID | // done |
| **DELETE** | `/api/faq/<int:id>/delete/` | Delete an FAQ by ID | // done |

## Contribution
Feel free to contribute! Fork the repository, make changes, and create a pull request.

## License
This project is licensed under the **MIT License**.

