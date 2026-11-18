from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from . import Base, Post, User


class Reaction(Base):
    __tablename__ = "reactions"

    post_id = Column(String, ForeignKey(Post.post_id), primary_key=True, nullable=False)
    username = Column(String, ForeignKey(User.username), primary_key=True, nullable=False)

    reaction_type = Column(String, nullable=False)