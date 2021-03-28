from typing import List
from sqlalchemy.orm import Session
from app.dependencies import get_db
from ..cruds import project_type as project_type_crud, ProjectTypeEdit, get_project_type_by_id, edit_project_type, \
    delete_project_type_by_id
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


@router.patch("/project_type/{project_id}", response_model=ProjectTypeResponse)
async def edit_projects_type(
        project_id: int,
        data: ProjectTypeEdit = Depends(ProjectTypeEdit.as_form),
        image: UploadFile = File(default=None),
        db: Session = Depends(get_db)
):
    try:
        project_type = get_project_type_by_id(db, project_id)
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                   "can be up to " + str(max_image_size_KB) + " KB",
        )

    if project_type is None:
        raise HTTPException(status_code=404, detail="project type not found")

    try:
        project_type_response = await edit_project_type(db, project_type, data, image)
    except ImageException:
        raise HTTPException(
            status_code=400,
            detail="You must sent correct image (only MIME image/jpg and image/png) and image size "
                   "can be up to " + str(max_image_size_KB) + " KB",
        )
    return project_type_response


@router.delete("/project_type/{project_type_id}")
async def delete_projects(
        project_type_id: int,
        db: Session = Depends(get_db)
):
    project_type = get_project_type_by_id(db, project_type_id)
    if project_type is None:
        raise HTTPException(status_code=404, detail="project type not found")
    delete_project_type_by_id(db, project_type)

    return HTTPException(status_code=200, detail="Project type deleted")
