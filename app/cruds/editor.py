from sqlalchemy.orm import Session

from .. import models
from ..schemats.editor import EditorCreate, EditorResponse, EditorEdit


def get_editors(db: Session, skip: int = 0, limit: int = 100):
    editors = db.query(models.editors.Editors).offset(skip).limit(limit).all()

    return editors


def get_editor_by_id(db: Session, editor_id: int):
    editor = db.query(models.editors.Editors).filter(models.editors.Editors.id == editor_id).first()

    return editor


async def create_editor(db: Session, editor: EditorCreate):
    db_editor = models.editors.Editors(**editor.dict())
    db.add(db_editor)
    db.commit()
    db.refresh(db_editor)
    return db_editor


async def edit_editor(db: Session, editor: EditorResponse, data: EditorEdit):
    if data.name is not None:
        editor.name = data.name

    if data.src is not None:
        editor.src = data.src

    db.commit()
    db.refresh(editor)
    return editor


def delete_editor_by_id(db: Session, editor: EditorResponse):
    projects = db.query(models.Project).filter(models.Project.editor_id == editor.id).all()
    for project in projects:
        project.editor_id = None
    db.commit()

    db.delete(editor)
    db.commit()
