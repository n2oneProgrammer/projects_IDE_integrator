from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemats.project import ProjectResponse, ProjectCreate, ProjectEdit
from ..cruds import project as project_crud, get_project_by_id, edit_project
from ..file_service import ImageException, max_image_size_KB

router = APIRouter(tags=["project"])


@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return project_crud.get_projects(db, skip, limit)


@router.post("/projects", response_model=ProjectResponse)
async def get_projects(
        project: ProjectCreate = Depends(ProjectCreate.as_form),
        image: UploadFile = File(default=None),
        db: Session = Depends(get_db)
):
    try:
        project = await project_crud.create_project(db, project, image)
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
    return project


@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def get_projects(
        project_id: int,
        data: ProjectEdit = Depends(ProjectEdit.as_form),
        image: UploadFile = File(default=None),
        db: Session = Depends(get_db)
):
    try:
        project = get_project_by_id(db, project_id)
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                   "can be up to " + str(max_image_size_KB) + " KB",
        )

    if project is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        project_response = await edit_project(db, project, data, image)
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                   "can be up to " + str(max_image_size_KB) + " KB",
        )
    return project_response
