from sqlalchemy import ARRAY, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base


class Inventory(Base):
    title = Column(String)
    description = Column(String)
    media_links = Column(ARRAY(String))
    task_id = Column(ForeignKey("tasks.id"), nullable=False)

    task = relationship("Task", back_populates="inventory")
    inventory_users = relationship("InventoryUser", back_populates="inventory")
