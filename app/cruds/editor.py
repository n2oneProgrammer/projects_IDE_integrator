from sqlalchemy.orm import Session

from .. import models


def get_editors(db: Session, skip: int = 0, limit: int = 100):
    editors = db.query(models.editors.Editors).offset(skip).limit(limit).all()

    return editors


def get_editor_by_id(db: Session, editor_id: int):
    editor = db.query(models.editors.Editors).filter(models.editors.Editors.id == editor_id).first()

    return editor
