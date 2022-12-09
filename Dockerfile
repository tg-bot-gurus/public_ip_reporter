# Base image
FROM python:alpine

# Maintainer
LABEL "Maintainer"="David Kurasov (david.kurasov@mail.ru)"

# Add app code to /code inside container image
ADD . /app

# Set working directory for subsequent commands
WORKDIR /app

# Install dependencies
RUN pip3 install -r requirements.txt

# Command to run when container starts
ENTRYPOINT ["python3", "public_ip_reporter.py"]