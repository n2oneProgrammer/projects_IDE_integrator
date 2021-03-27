from sqlalchemy import Column, ForeignKey, Integer, String, orm, event
from sqlalchemy.orm import relationship
from ..database import Base
from ..file_service import remove_image


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(500))
    color = Column(String(6), default="000000")
    image = Column(String(300), nullable=True)
    type_id = Column(Integer, ForeignKey("project_type.id"))
    editor_id = Column(Integer, ForeignKey("editor.id"), nullable=True)

    type = relationship("ProjectType", back_populates="projects", cascade="save-update")
    editor = relationship("Editors")

    def get_correct(self):
        if self.color is None:
            self.color = self.type.color
        if self.image is None:
            self.image = self.type.default_image
        if self.editor is None:
            self.editor = self.type.default_editor
        return self


@event.listens_for(Project, 'before_delete')
def receive_before_delete(mapper, connection, target):
    if target.image is not None:
        remove_image(target.image)
