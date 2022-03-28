FROM fedora:latest
WORKDIR /app
RUN curl -sSL https://install.python-poetry.org | python3.9 -
ENV PATH="${HOME}/.local/bin:${PATH}"
COPY . .
RUN poetry install
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=todolist.settings.production" ]
