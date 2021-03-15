from fastapi import Form
from pydantic import BaseModel

from app.dependencies import color_regex
from app.schemats.editor import EditorResponse


class ProjectTypeResponse(BaseModel):
    id: int
    name: str
    color: str
    default_image: str
    default_editor: EditorResponse

    class Config:
        orm_mode = True


class ProjectTypeCreate(BaseModel):
    name: str
    color: str
    default_editor_id: int

    @classmethod
    def as_form(
            cls,
            name: str = Form(..., min_length=1, max_length=100),
            color: str = Form(..., regex=color_regex),
            default_editor_id: int = Form(...)
    ):
        return cls(
            name=name,
            color=color,
            default_editor_id=default_editor_id
        )

    class Config:
        orm_mode = True
