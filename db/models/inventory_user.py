from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class InventoryUser(Base):
    user_id = Column(ForeignKey("users.id"), nullable=False)
    inventory_id = Column(ForeignKey("inventorys.id"), nullable=False)
    ending = Column(Boolean)

    user = relationship("User", back_populates="inventory_users")
    inventory = relationship("Inventory", back_populates="inventory_users")
