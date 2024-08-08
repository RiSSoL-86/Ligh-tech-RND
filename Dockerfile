FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry
RUN poetry install --no-dev

COPY . /app/

CMD ["poetry", "run", "python", "app/manage.py", "runserver", "0.0.0.0:5000"]
