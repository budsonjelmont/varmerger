#FROM python:3.9.10 #Doesn't work, pyVCF installation throws errors
FROM python:3.8.5

ARG CONTEXTPATH=/app/flask

WORKDIR usr/src/flask
COPY requirements.txt .
COPY setup.py .
COPY varchemist .
RUN pip install --no-cache-dir -r requirements.txt && python3 setup.py develop
COPY ${CONTEXTPATH} .
RUN pip install --no-cache-dir -r requirements.txt
