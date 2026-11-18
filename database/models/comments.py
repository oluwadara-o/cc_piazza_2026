from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from . import Base, User, Post


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, ForeignKey(Post.post_id), nullable=False)
    username = Column(String, ForeignKey(User.username), nullable=False)

    comment_text = Column(String, nullable=False)
    comment_ts = Column(DateTime, nullable=False)
