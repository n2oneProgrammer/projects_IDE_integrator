from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from ..cruds import editor as editor_crud
from ..schemats.editor import EditorResponse, EditorCreate

router = APIRouter(tags=["editor"])


@router.get("/editors", response_model=List[EditorResponse])
async def get_editors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return editor_crud.get_editors(db, skip, limit)


@router.post("/editors", response_model=EditorResponse)
async def create_editor(
        project: EditorCreate = Depends(EditorCreate.as_form),
        db: Session = Depends(get_db)
):
    try:
        project = await editor_crud.create_editor(db, project)
    except Exception as a:
        raise HTTPException(
            status_code=400,
            detail=str(a)
        )
    return project
