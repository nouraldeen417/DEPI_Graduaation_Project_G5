# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Change the working directory to the Django app subdirectory
WORKDIR /app/djangoapp

# Collect static files
RUN python manage.py collectstatic --noinput
# # Command to run the application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Expose the port the app runs on
EXPOSE 8000
# Run Gunicorn directly in the Docker image
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "storefront.wsgi:application"]