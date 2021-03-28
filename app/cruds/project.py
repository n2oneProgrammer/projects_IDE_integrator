from fastapi import UploadFile
from sqlalchemy.orm import Session

from .editor import get_editor_by_id
from .project_type import get_project_type_by_id
from .. import models
from ..file_service import upload_image, reupload_image
from ..schemats.project import ProjectCreate, ProjectEdit, ProjectResponse


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    projects = db.query(models.project.Project).offset(skip).limit(limit).all()

    return [project.get_correct() for project in projects]


def get_project_by_id(db: Session, project_id: int):
    project = db.query(models.project.Project).filter(models.project.Project.id == project_id).first()

    return project.get_correct()


async def create_project(db: Session, project: ProjectCreate, image: UploadFile = None):
    image_url = None
    if project.editor_id is not None and get_editor_by_id(db, project.editor_id) is None:
        raise Exception("Editor with id " + str(project.editor_id) + " not exist")

    if get_project_type_by_id(db, project.type_id) is None:
        raise Exception("type with id " + str(project.type_id) + " not exist")
    if image is not None:
        image_url = await upload_image(image)

    db_project = models.project.Project(**project.dict(), image=image_url)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project.get_correct()


async def edit_project(db: Session, project: ProjectResponse, data: ProjectEdit, image: UploadFile = None):
    if data.editor_id is not None and get_editor_by_id(db, data.editor_id) is None:
        raise Exception("Editor with id " + str(data.editor_id) + " not exist")
    else:
        project.editor = get_editor_by_id(db, data.editor_id)
    if data.type_id is not None and get_project_type_by_id(db, data.type_id) is None:
        raise Exception("type with id " + str(data.type_id) + " not exist")
    else:
        project.type = get_project_type_by_id(db, data.type_id)
    if image is not None:
        image_url = await reupload_image(project.image, image)
        project.image = image_url

    if data.name is not None:
        project.name = data.name

    if data.description is not None:
        project.description = data.description

    if data.color is not None:
        project.color = data.color

    db.commit()
    db.refresh(project)
    return project.get_correct()


def delete_project_by_id(db: Session, project: ProjectResponse):
    db.delete(project)
    db.commit()
