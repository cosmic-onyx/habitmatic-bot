FROM python:3.13-slim

WORKDIR /usr/app

ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONPATH=/usr/app/src

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry --version

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root&& \
    rm -rf $POETRY_CACHE_DIR

COPY . .