FROM python:3.9

RUN useradd python-user

ADD --chown=python-user:python-user user-service.tgz /usr/local/user-service/
RUN pip install -r /usr/local/user-service/Requirements.txt

USER python-user

WORKDIR /usr/local/user-service/src

ENTRYPOINT ["python", "app.py", "--aws"]