from typing import List
from sqlalchemy.orm import Session
from app.dependencies import get_db
from ..cruds import project_type as project_type_crud
from ..file_service import ImageException, max_image_size_KB
from ..schemats.project_type import ProjectTypeResponse, ProjectTypeCreate
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

router = APIRouter(tags=["project type"])


@router.get("/project_type", response_model=List[ProjectTypeResponse])
async def get_project_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return project_type_crud.get_project_types(db, skip, limit)


@router.post("/project_type", response_model=ProjectTypeResponse)
async def create_project_types(data: ProjectTypeCreate = Depends(ProjectTypeCreate.as_form),
                               default_image: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        project_type = await project_type_crud.create_project_type(db, data, default_image)
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                   "can be up to " + str(max_image_size_KB) + " KB",
        )
    except Exception as a:
        raise HTTPException(
            status_code=400,
            detail=str(a)
        )

    return project_type
