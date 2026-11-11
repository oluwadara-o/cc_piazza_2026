from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from . import Base

class Reaction(Base):
    __tablename__ = "reactions"

    post_id = Column(String, primary_key=True, foiegn_key=ForeignKey("posts.post_id"), nullable=False)
    username = Column(String, primary_key=True, foiegn_key=ForeignKey("users.username"), nullable=False)

    reaction_type = Column(String, nullable=False)