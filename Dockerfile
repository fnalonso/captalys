FROM python:3.7.7-alpine

RUN mkdir /opt/api

WORKDIR /opt/api

ADD . .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

EXPOSE 8080

#ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8080" ,"--wsgi-file", "backend/app.py", "--callable", "app", "--py-autoreload", "1"]
ENTRYPOINT ["./scripts/start.sh"]