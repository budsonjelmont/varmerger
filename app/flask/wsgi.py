from app import app, setup_logging, setup_phasing

if __name__ == "__main__":
    # Will run the app using flask's development server
    setup_logging('config/log_config.yaml')
    setup_phasing('config/phase_config.yaml')
    app.run(host='0.0.0.0', port=6666)
