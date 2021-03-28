from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from ..cruds import editor as editor_crud, get_editor_by_id, edit_editor, delete_editor_by_id
from ..schemats.editor import EditorResponse, EditorCreate, EditorEdit

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


@router.patch("/editors/{editor_id}", response_model=EditorResponse)
async def edit_projects(
        editor_id: int,
        data: EditorEdit = Depends(EditorEdit.as_form),
        db: Session = Depends(get_db)
):
    editor = get_editor_by_id(db, editor_id)
    if editor is None:
        raise HTTPException(status_code=404, detail="project not found")

    editor_response = await edit_editor(db, editor, data)
    return editor_response


@router.delete("/editors/{editor_id}")
async def delete_editor(
        editor_id: int,
        db: Session = Depends(get_db)
):
    editor = get_editor_by_id(db, editor_id)
    if editor is None:
        raise HTTPException(status_code=404, detail="Editor not found")
    delete_editor_by_id(db, editor)

    return HTTPException(status_code=200, detail="Editor deleted")
