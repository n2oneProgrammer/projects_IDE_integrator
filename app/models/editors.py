from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Editors(Base):
    __tablename__ = "editor"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    src = Column(String(300))

    types = relationship("ProjectType", back_populates="default_editor", cascade="all, delete")
