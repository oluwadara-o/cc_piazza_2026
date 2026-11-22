from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from . import Base, Post, User


class Topic(Base):
    __tablename__ = "topics"

    post_id = Column(String, ForeignKey(Post.post_id), primary_key=True, nullable=False)
    topic_name = Column(String, primary_key=True, nullable=False)