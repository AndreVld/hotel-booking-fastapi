from sqlalchemy import JSON, Column, Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


# class Hotels(Base):
#     __tablename__ = 'hotels'
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     locations = Column(String, nullable=False)
#     services = Column(JSON)
#     rooms_quantity = Column(Integer, nullable=False)
#     image_id = Column(Integer)

class Hotels(Base):
    __tablename__ = 'hotels'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    locations: Mapped[str] = mapped_column( nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]