Service for merging multiple variants in VCF format into a single VCF record

# App configuration

The application is configured through a combination of external configuration files and environment variables.

# To run

## Using the flask built-in dev server

	python3 app.py ${config name, one of "dev","prod","development","production", or "default"}

## Gunicorn

	VARMERGER_CONFIGNAME=${config name, one of "dev","prod","development","production", or "default"} gunicorn --bind 0.0.0.0:5000 wsgi:app

## Behind nginx in container


