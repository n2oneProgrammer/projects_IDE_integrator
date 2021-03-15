from typing import Optional

from fastapi import Query, Form
from pydantic import BaseModel, Field

from app.dependencies import color_regex
from app.schemats.editor import EditorResponse
from app.schemats.project_type import ProjectTypeResponse


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    color: str = None
    image: str = None
    type: ProjectTypeResponse
    editor: EditorResponse = None

    def get_correct(self):
        if self.color is None:
            self.color = self.type.color
        if self.image is None:
            self.image = self.type.default_image
        if self.editor is None:
            self.editor = self.type.default_editor
        return self

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    name: str = Query(None, min_length=10, max_length=100)
    description: str = Query(None, max_length=500)
    color: Optional[str] = Query(None, regex=color_regex)
    type_id: int
    editor_id: Optional[int]

    @classmethod
    def as_form(
            cls,
            name: str = Form(..., min_length=10, max_length=100),
            description: str = Form(..., max_length=500),
            color: Optional[str] = Form(None, regex=color_regex),
            type_id: int = Form(...),
            editor_id: Optional[int] = Form(None),
    ):
        return cls(
            name=name,
            description=description,
            color=color,
            type_id=type_id,
            editor_id=editor_id
        )

    class Config:
        orm_mode = True


class ProjectEdit(BaseModel):
    name: Optional[str] = Query(None, min_length=10, max_length=100)
    description: Optional[str] = Query(None, max_length=500)
    color: Optional[str] = Query(None, regex=color_regex)
    type_id: Optional[int]
    editor_id: Optional[int]

    @classmethod
    def as_form(
            cls,
            name: Optional[str] = Form(None, min_length=10, max_length=100),
            description: Optional[str] = Form(None, max_length=500),
            color: Optional[str] = Form(None, regex=color_regex),
            type_id: Optional[int] = Form(None),
            editor_id: Optional[int] = Form(None),
    ):
        return cls(
            name=name,
            description=description,
            color=color,
            type_id=type_id,
            editor_id=editor_id
        )

    class Config:
        orm_mode = True
