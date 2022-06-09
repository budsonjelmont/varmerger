from app import app, setup_logging

if __name__ == "__main__":
    # Will run the app using flask's development server
    setup_logging('config/log_config.yaml')
    app.run(host='0.0.0.0', port=6666)
