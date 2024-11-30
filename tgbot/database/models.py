from datetime import datetime
# from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship



engine = create_async_engine("sqlite+aiosqlite:///bot.db")

session = async_sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    # id: Mapped[int] = mapped_column(unique=True, autoincrement=True, primary_key=True)
    user_tg_id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(unique=True)
    forms: Mapped[list['UserForms']] = relationship(uselist=True, back_populates="user", lazy='joined')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class UserForms(Base):
    __tablename__ = 'forms'
    id: Mapped[int] = mapped_column(unique=True, primary_key=True, autoincrement=True)
    user: Mapped[User] = relationship(uselist=False, back_populates='forms')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_tg_id', ondelete='cascade'))
    name: Mapped[str]
    latitude: Mapped[str]
    longitude: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    price: Mapped[str]

    def __repr__(self):
        return f"UserForms(id={self.id}, name={self.name}, created_at={self.created_at})"

    # def __str__(self):
        # return f"{self.name} (ID: {self.id})"