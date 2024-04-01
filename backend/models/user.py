from sqlalchemy.orm import Mapped

from .base import Base


class User(Base):
    __tablename__ = "user"

    email: Mapped[str]
    password: Mapped[str]
