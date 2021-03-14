from pydantic import BaseModel

from app.schemats.editor import EditorResponse


class ProjectTypeResponse(BaseModel):
    id: int
    name: str
    color: str
    default_image: str
    default_editor: EditorResponse

    class Config:
        orm_mode = True
