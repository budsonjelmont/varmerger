from app import server

if __name__ == "__main__":
    # Will run the app using flask's development server 
    server.run(host='0.0.0.0', port=6666)
