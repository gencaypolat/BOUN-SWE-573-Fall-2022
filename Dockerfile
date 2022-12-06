# Pull base image
FROM python:3.8-slim-buster

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Copy project
COPY . .

ENTRYPOINT ["python","manage.py","runserver","0.0.0.0:8000"]








# FROM python:3.8-slim-buster

# WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

# COPY . .

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


# FROM python:3.8

# ENV PYTHONUNBUFFERED = 1

# WORKDIR /wire_project

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
