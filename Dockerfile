# Choose base image as python
FROM python:3.11

# install pipenv
RUN pip install pipenv

# copy to /app and set working directory
COPY . /app
WORKDIR /app

# Install dependencies
RUN pipenv install

# Expose port 5001
EXPOSE 5001

CMD ["pipenv", "run", "python", "app.py"]