from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string
import random
from pymongo import MongoClient
from fastapi.responses import RedirectResponse

app = FastAPI()
CURRENT_URL = "http://127.0.0.1:8000"
db_url = "mongodb+srv://<URL_HERE>"

client = MongoClient(db_url)
db = client["url_shortener"]
collection = db["url_mappings"]


class URLMapping(BaseModel):
    url: str


def generate_short_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=6))
    return code


@app.get("/{code}")
def redirect_url(code: str):
    mapping = collection.find_one({"code": code})
    if mapping:
        return RedirectResponse(mapping["url"])
    else:
        raise HTTPException(status_code=404, detail="URL not found.")


@app.post("/shorten")
def shorten_url(mapping: URLMapping):
    code = generate_short_code()
    collection.insert_one({"code": code, "url": mapping.url})
    return {"shortened_url": f"{CURRENT_URL}/{code}"}

