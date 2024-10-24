from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HistoryModel(Base):
    __tablename__ = "histories"
    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    file_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.file_url = kwargs.get("file_url")
