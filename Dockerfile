FROM python:3.10-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --no-input

# Wait for db before starting
RUN apt-get update && apt-get install -y netcat
RUN chmod +x ./wait_for_db.sh


# Use the script to wait for the database before starting Django
ENTRYPOINT ["sh", "./wait_for_db.sh", "postgres"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

