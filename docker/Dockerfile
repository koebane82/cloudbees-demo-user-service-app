FROM python:3.9

RUN useradd python-user

ADD --chown=python-user:python-user user-service.tgz /usr/local/user-service

WORKDIR /usr/local/user-service/app

ENTRYPOINT ["python", "app.py", "--aws"]