from sqlalchemy import ARRAY, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base


class Hint(Base):
    title = Column(String, nullable=False)
    text = Column(String)
    media_links = Column(ARRAY(String))
    task_id = Column(ForeignKey("tasks.id"), nullable=False)

    task = relationship("Task", back_populates="hints")
