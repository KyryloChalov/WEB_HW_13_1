from datetime import date
from sqlalchemy import Integer, String, DateTime, Date, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.sql.schema import ForeignKey
from static.constants import NAME_LEN, EMAIL_LEN, PHONE_LEN, NOTES_LEN


class Base(DeclarativeBase):
    ...


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(NAME_LEN), nullable=False)
    last_name: Mapped[str] = mapped_column(String(NAME_LEN))
    email: Mapped[str] = mapped_column(String(EMAIL_LEN))
    phone: Mapped[str] = mapped_column(String(PHONE_LEN))
    birthday: Mapped[date] = mapped_column(Date())
    notes: Mapped[str] = mapped_column(String(NOTES_LEN), nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), default=1
    )
    user = relationship("User", backref="contacts")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(NAME_LEN))
    email: Mapped[str] = mapped_column(String(EMAIL_LEN), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(NOTES_LEN), nullable=False)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    refresh_token: Mapped[str] = mapped_column(String(NOTES_LEN), nullable=True)
    avatar: Mapped[str] = mapped_column(String(NOTES_LEN), nullable=True)
    confirmed = mapped_column(Boolean, default=False)
