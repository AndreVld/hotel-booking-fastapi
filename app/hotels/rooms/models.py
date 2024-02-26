from sqlalchemy import  JSON, ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Rooms(Base):
    __tablename__ = 'rooms'
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    hotel: Mapped['Hotels'] = relationship(back_populates='rooms')
    bookings: Mapped[list['Bookings']] = relationship(back_populates='room')


    def __str__(self) -> str:
        return f'{self.name}'