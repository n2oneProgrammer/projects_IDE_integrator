from sqlalchemy import Column, ForeignKey, Integer, String, event
from sqlalchemy.orm import relationship

from ..database import Base
from ..file_service import remove_image


class ProjectType(Base):
    __tablename__ = "project_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    color = Column(String(6))
    default_image = Column(String(300))
    default_editor_id = Column(Integer, ForeignKey("editor.id"))
    default_editor = relationship("Editors", back_populates="types", cascade="save-update")

    projects = relationship("Project", back_populates="type", cascade="all, delete")


@event.listens_for(ProjectType, 'before_delete')
def receive_before_delete(mapper, connection, target):
    if target.default_image is not None:
        remove_image(target.default_image)
