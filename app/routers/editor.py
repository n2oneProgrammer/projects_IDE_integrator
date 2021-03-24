from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from ..cruds import editor as editor_crud
from ..schemats.editor import EditorResponse

router = APIRouter(tags=["editor"])


@router.get("/editors", response_model=List[EditorResponse])
async def get_editors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return editor_crud.get_editors(db, skip, limit)

