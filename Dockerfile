FROM python:3.8

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip

RUN pip install --upgrade setuptools

RUN pip install ez_setup

RUN pip install -r requirements.txt




# FROM python:3
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . /code/
# ENTRYPOINT ["./entrypoint.sh"] 
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]








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