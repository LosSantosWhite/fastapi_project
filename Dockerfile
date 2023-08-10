FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code/
COPY poetry.lock /code/
RUN pip install poetry==1.5.1
RUN poetry install
COPY . /code/