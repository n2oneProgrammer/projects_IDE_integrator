from fastapi import UploadFile
from sqlalchemy.orm import Session

from .editor import get_editor_by_id
from .. import models
from ..file_service import upload_image, reupload_image
from ..schemats.project_type import ProjectTypeCreate, ProjectTypeResponse, ProjectTypeEdit


def get_project_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.project_type.ProjectType).offset(skip).limit(limit).all()


def get_project_type_by_id(db: Session, project_id: int):
    editor = db.query(models.project_type.ProjectType).filter(models.project_type.ProjectType.id == project_id).first()

    return editor


async def create_project_type(db: Session, data: ProjectTypeCreate, image: UploadFile = None):
    image_url = None
    if get_editor_by_id(db, data.default_editor_id) is None:
        raise Exception("Editor with id " + str(data.default_editor_id) + " not exist")
    if image is not None:
        image_url = await upload_image(image)

    db_project_type = models.project_type.ProjectType(**data.dict(), default_image=image_url)
    db.add(db_project_type)
    db.commit()
    db.refresh(db_project_type)
    return db_project_type


async def edit_project_type(db: Session, project: ProjectTypeResponse, data: ProjectTypeEdit, image: UploadFile = None):
    if data.default_editor_id is not None:
        editor = get_editor_by_id(db, data.default_editor_id)
        if editor is None:
            raise Exception("Editor with id " + str(data.default_editor_id) + " not exist")
        project.default_editor = editor

    if image is not None:
        image_url = await reupload_image(project.default_image, image)
        project.default_image = image_url

    if data.name is not None:
        project.name = data.name

    if data.color is not None:
        project.color = data.color

    db.commit()
    db.refresh(project)
    return project


def delete_project_type_by_id(db: Session, project_type: ProjectTypeResponse):
    db.delete(project_type)
    db.commit()
