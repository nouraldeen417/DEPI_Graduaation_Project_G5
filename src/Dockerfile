# Use an official Python runtime as a parent image
FROM python:3.11-slim 
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && python djangoapp/manage.py collectstatic --noinput  

EXPOSE 8000
# Change the working directory to the Django app subdirectory
WORKDIR /app/djangoapp
# Run Gunicorn directly in the Docker image
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "storefront.wsgi:application"]
