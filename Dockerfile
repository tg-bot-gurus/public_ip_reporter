# Base image
FROM python:alpine

# Maintainer
LABEL "Maintainer"="TG Bot Guru :)"

# Add app code to /app inside container image
ADD . /app

# Set working directory for subsequent commands
WORKDIR /app

# Install dependencies
RUN pip3 install -r requirements.txt

# Command to run when container starts
ENTRYPOINT ["python3", "public_ip_reporter.py"]