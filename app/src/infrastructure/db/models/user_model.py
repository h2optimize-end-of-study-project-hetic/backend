from sqlmodel import SQLModel, Field

class UserModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
