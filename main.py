from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Minimal FastAPI Backend")

# Allow all origins (mude para produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store (exemplo)
DB = {}

class Item(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., ge=0)

@app.get("/")
async def root():
    return {"message": "Hello from Minimal FastAPI Backend"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    item = DB.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", status_code=201)
async def create_item(item: Item):
    item_id = item.id or str(uuid4())
    item.id = item_id
    DB[item_id] = item.dict()
    return DB[item_id]