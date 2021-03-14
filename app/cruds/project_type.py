from sqlalchemy.orm import Session

from .. import models


def get_editor_by_id(db: Session, editor_id: int):
    editor = db.query(models.editors.Editors).filter(models.editors.Editors.id == editor_id).first()

    return editor
