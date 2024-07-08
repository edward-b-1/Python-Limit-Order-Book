
from fastapi import FastAPI
from pydantic import BaseModel

from my_package import my_value

import os

print(f'__name__={__name__}')
print(os.getcwd())
print(os.environ['PYTHONPATH'])

app = FastAPI()

class FastAPI_Value(BaseModel):
    value: int

@app.post('/')
def root(fastapi_value: FastAPI_Value):
    print(fastapi_value)
    next_value = fastapi_value.value + my_value
    print(next_value)
    #next_value = fastapi_value.value
    return {
        'next_value': next_value
    }

