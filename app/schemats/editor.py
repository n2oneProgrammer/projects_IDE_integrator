from typing import Optional

from fastapi import Query, Form
from pydantic import BaseModel


class EditorResponse(BaseModel):
    id: int
    name: str
    src: str

    class Config:
        orm_mode = True


class EditorCreate(BaseModel):
    name: str = Query(..., min_length=5, max_length=100)
    src: str = Query(..., min_length=5, max_length=300)

    @classmethod
    def as_form(
            cls,
            name: str = Form(..., min_length=5, max_length=100),
            src: str = Form(..., min_length=5, max_length=300),

    ):
        return cls(
            name=name,
            src=src
        )

    class Config:
        orm_mode = True


class EditorEdit(BaseModel):
    name: Optional[str] = Query(None, min_length=5, max_length=100)
    src: Optional[str] = Query(None, min_length=5, max_length=300)

    @classmethod
    def as_form(
            cls,
            name: str = Form(None, min_length=5, max_length=100),
            src: str = Form(None, min_length=5, max_length=300),

    ):
        return cls(
            name=name,
            src=src
        )

    class Config:
        orm_mode = True
