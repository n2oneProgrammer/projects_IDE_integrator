from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class ProjectType(Base):
    __tablename__ = "project_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    color = Column(String(6))
    default_image = Column(String(300))
    default_editor_id = Column(Integer, ForeignKey("editor.id"))
    default_editor = relationship("Editors")
