FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app
# ADD requirements.txt /code/
COPY requirements.txt /app
RUN pip install -r requirements.txt
# ADD . /code/
COPY . /app