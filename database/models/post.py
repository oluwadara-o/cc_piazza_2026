from sqlalchemy import Column, Integer, String, ForeignKey

from database.database import Base


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, foiegn_key=ForeignKey("users.username"), nullable=False)

    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    creation_ts = Column(String, nullable=False)
    expiration_ts = Column(String, nullable=False)