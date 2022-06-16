#FROM python:3.9.10 #Doesn't work, pyVCF installation throws errors
FROM python:3.8.5

ARG APP_PATH_EXT=/app/flask
ARG APP_PATH_INT=/usr/src/flask
ARG PKG_PATH_INT=${APP_PATH_INT}/varchemist

#WORKDIR usr/src/flask
WORKDIR ${APP_PATH_INT}
COPY varchemist ${PKG_PATH_INT}
COPY requirements.txt ${PKG_PATH_INT}
COPY setup.py ${PKG_PATH_INT}
COPY ${APP_PATH_EXT} .
RUN pip install --no-cache-dir -r requirements.txt && python3 ${PKG_PATH_INT}/setup.py install && pip install --no-cache-dir -r ${PKG_PATH_INT}/requirements.txt
