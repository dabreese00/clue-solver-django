FROM python:3
ENV PYTHONBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
WORKDIR /code/cluesolver
RUN python manage.py collectstatic
