import hashlib
import os
import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")


class Body(BaseModel):
    length: Union[int, None] = 20


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    return {'token': string}

""" 
Create an pydantic model for Text, which has a single attribute text of type str.
"""


class Text(BaseModel):
    text: str


# Create a FastAPI endpoint that accepts a POST request with a JSON body containing a single field called "text" and returns a checksum of the text. The endpoint should be /docs. Write the function that returns the checksum of the text.


@app.post('/docs')
def docs(text: str):
    """
    return a checksum of field 'text'. Example POST request body:

    {
        "checksum": 3b8b91c75627bee566dcb88f4805901b20a3eab2520bcff8d26c87157a035026
    }
    """
    return {'checksum': hashlib.sha256(text.encode('utf-8')).hexdigest()}