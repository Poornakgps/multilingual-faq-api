FROM python:3.10

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Run migrations before starting the server
CMD ["sh", "-c", "\
    python manage.py makemigrations faq && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000 \
"]


