# Need to doublecheck if 3.9 works now after pyVCF3 upgrdate
FROM python:3.9.10
# FROM python:3.8.5

ARG APP_PATH_EXT=/app/flask
ARG APP_PATH_INT=/app
ARG PKG_PATH_INT=${APP_PATH_INT}/varmerger

#WORKDIR usr/src/flask
WORKDIR ${APP_PATH_INT}
COPY varmerger ${PKG_PATH_INT}
COPY requirements.txt ${PKG_PATH_INT}
COPY setup.py ${PKG_PATH_INT}
COPY ${APP_PATH_EXT} .
#TODO don't run as root
RUN pip install --no-cache-dir -r requirements.txt && python3 ${PKG_PATH_INT}/setup.py install && pip install --no-cache-dir -r ${PKG_PATH_INT}/requirements.txt

EXPOSE 6666

CMD ["gunicorn", "--bind", "0.0.0.0:6666", "wsgi:app"]