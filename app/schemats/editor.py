from pydantic import BaseModel


class EditorResponse(BaseModel):
    id: int
    name: str
    src: str

    class Config:
        orm_mode = True
