from sqlalchemy import Column, Integer, String
from ..database import Base


class Editors(Base):
    __tablename__ = "editor"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    src = Column(String(300))
