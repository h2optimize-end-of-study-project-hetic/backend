from sqlmodel import SQLModel, Field


class BuildingModel(SQLModel, table=True):
    __tablename__ = "building"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., nullable=False)
