#FROM python:3.9.10 #Doesn't work, pyVCF installation throws errors
FROM python:3.8.5

WORKDIR usr/src/flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
