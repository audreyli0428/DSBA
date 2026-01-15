from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Simple API")

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/health")
def health():
    return {"status": "ok"}

class Item(BaseModel):
    name: str
    price: float

@app.post("/predict")
def predict(item: Item):
    score = item.price * 0.1
    return {"name": item.name, "score": score}
