from app import init_app 

app = init_app('default')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6666)
