from sqlalchemy.orm import Session

from .. import models


def get_project_type_by_id(db: Session, project_id: int):
    editor = db.query(models.project_type.ProjectType).filter(models.project_type.ProjectType.id == project_id).first()

    return editor
