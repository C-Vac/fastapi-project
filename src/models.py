from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class Post(Base):
    """
    Summary:

        models.Post: direct ORM mapping to the postgres table


    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")

    title = Column(String, nullable=False)

    content = Column(String, nullable=False)

    published = Column(Boolean, server_default="TRUE", nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    owner = relationship("User")


class User(Base):
    """
    Summary:
        models.User: direct ORM mapping to the postgres table


    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
