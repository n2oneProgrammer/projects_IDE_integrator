from fastapi import UploadFile
from sqlalchemy.orm import Session

from .editor import get_editor_by_id
from .. import models
from ..file_service import upload_image
from ..schemats.project import ProjectCreate


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    projects = db.query(models.project.Project).offset(skip).limit(limit).all()

    return [project.get_correct() for project in projects]


async def create_project(db: Session, project: ProjectCreate, image: UploadFile = None):
    image_url = ""
    if image is not None:
        image_url = await upload_image(image)
    if get_editor_by_id(project.editor_id) is None:
        raise Exception("Editor with id " + str(project.editor_id) + " not exist")

    db_project = models.project.Project(**project.dict(), image=image_url)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
