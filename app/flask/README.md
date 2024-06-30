TODO

## Configuring the application

The application 
- On startup, the application accepts an environment/configuration key (see options defined `config/config.py`. Default: `default`).
- The key should resolve to a class defined in `config/config.py`. 
- The application will look for a file called `.env` and load any variables defined there.
- If any of variables `LOG_CONFIG_YAML_PATH`, `PHASE_CONFIG_YAML_PATH`, or `CORS_CONFIG_YAML_PATH` are populated, application component configs are read from there.
- Otherwise, the defaults in the appropriate config class from `config/config.py` are used.
