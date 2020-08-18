# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /teambuilder

# Install dependencies
COPY Pipfile Pipfile.lock /teambuilder/
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --system

# Now copy in our code, and run it
COPY . /teambuilder/
EXPOSE 8000