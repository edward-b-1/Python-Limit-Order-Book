
from fastapi import FastAPI

print(f'__name__={__name__}')

app = FastAPI()

@app.get('/')
def root():
    return {
        'example_key': 'example_value',
    }

