#
FROM python:3.11 as requirements-stage

#
WORKDIR /tmp

#
RUN pip install poetry

#
COPY ./pyproject.toml ./poetry.lock* /tmp/

#
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

#
FROM python:3.11

#
WORKDIR /code

#
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app app
COPY ./alembic alembic
COPY ./start.sh start.sh

#
# ARG DATABASE_URL
# ENV DATABASE_URL $DATABASE_URL

# run on port 8000 by default. to change add "--port", "80"
CMD ["./start.sh"]