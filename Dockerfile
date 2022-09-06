FROM python:3.8.4

USER root
WORKDIR /root

# bse
# RUN apt-get -y update
# RUN apt-get -y install python3-pip

# flask
COPY ./static/ /root/static/
COPY ./templates/ /root/templates/
COPY ./app.py /root/app.py
COPY ./requirements.txt /root/requirements.txt

RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt

RUN echo "db create"
RUN python -c "from app import db; db.create_all()"

ENV FLASK_APP=app

CMD flask run --host 0.0.0.0 -p 80
