from app import init_app 

app = init_app('config/log_config.yaml','config/phase_config.yaml')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6666)
