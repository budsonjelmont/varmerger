from os import path, getenv
from app import create_app 

configname = getenv('VARMERGER_CONFIGNAME') or 'default'

app = create_app(configname)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6666)
