
from flask import Flask, request

print(f'__name__={__name__}')

class FakeDB():

    def __init__(self) -> None:
        print(f'FakeDB.__init__')
        self.db = {}

db = FakeDB()

app = Flask(__name__)

@app.get('/get')
def get():
    content = request.json
    key = content.get('key')
    value = db.db.get(key)
    print(f'get: key={key} value={value}')
    return {
        'value': value,
    }

@app.post('/put')
def put():
    content = request.json
    key = content.get('key')
    value = content.get('value')
    print(f'put: key={key} value={value}')
    db.db[key] = value
    return {
        'status': 'ok',
    }