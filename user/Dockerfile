FROM python:3.9-slim

# Install dos2unix
RUN apt-get update && apt-get install -y dos2unix

# Upgrade pip
RUN pip install --upgrade pip

# Create a directory for the application
RUN mkdir /code

# Set the working directory to /app
WORKDIR /app

# Copy the current context into the /app directory in the container
COPY . .

# Convert all .py files to Unix-style line endings
RUN find . -type f -name "*.py" -exec dos2unix {} \;

# Fix shebang lines
RUN sed -i 's/\r$//' manage.py
RUN sed -i 's/\r$//' user/wsgi.py

# Uninstall any existing psycopg2 packages
RUN pip uninstall -y psycopg2 psycopg2-binary

# Install the required Python packages
RUN pip install --default-timeout=200 -r requirements.txt

# Expose port 8001
EXPOSE 8001

# Default command to run the application
CMD ./manage.py migrate && \
    gunicorn user.wsgi:application --bind 0.0.0.0:8001
