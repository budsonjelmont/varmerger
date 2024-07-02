TODO

Service for merging multiple variants in VCF format into a single VCF record

# To run

## Using the flask built-in dev server

	python3 app.py ${config name, one of "dev","prod","development","production", or "default"}

or equivalently:

    VARMERGER_CONFIGNAME=${config name, one of "dev","prod","development","production", or "default"} py wsgi.py

## Behind Gunicorn

	VARMERGER_CONFIGNAME=${config name, one of "dev","prod","development","production", or "default"} gunicorn --bind 0.0.0.0:6666 wsgi:app

## Behind nginx in container

TODO

## Configuring the application

The application is configured through a combination of external configuration files and environment variables.
- On startup, the application accepts an environment/configuration key that is provided to `create_app()`. The configuration key should resolve to a configuration class defined in config file `config/config.py` (Default: `default`).
    - When starting the application via `wsgi.py`, the `VARMERGER_CONFIGNAME` environment variable can be used to specify the configuration key.
- On import, the config file will check for the presence of a `.env` file located in the same directory and load any variables defined there.
- If any of the environment variables `LOG_CONFIG_YAML_PATH`, `PHASE_CONFIG_YAML_PATH`, or `CORS_CONFIG_YAML_PATH` are populated, the application will read the YAML files at the provided location(s) and use the values provided there as the application component configurations in lieu of the defaults in the specified config class.
- Otherwise, the defaults in the appropriate config class from `config/config.py` are used.
