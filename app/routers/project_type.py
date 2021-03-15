from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from ..cruds import project_type as project_type_crud
from ..schemats.project_type import ProjectTypeResponse

router = APIRouter(tags=["project type"])


@router.get("/project_type", response_model=List[ProjectTypeResponse])
async def get_project_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return project_type_crud.get_project_types(db, skip, limit)

