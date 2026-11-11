from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from . import Base, Post, User


class Reaction(Base):
    __tablename__ = "reactions"

    post_id = Column(String, primary_key=True, foiegn_key=Post.post_id, nullable=False)
    username = Column(String, primary_key=True, foiegn_key=User.username, nullable=False)

    reaction_type = Column(String, nullable=False)