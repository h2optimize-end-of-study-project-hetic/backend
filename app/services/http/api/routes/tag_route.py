from pydantic import BaseModel


class Tag(BaseModel):
    name: str
    source_address: str

@app.post("/items/")
async def create_item(item: Item):
    return item
