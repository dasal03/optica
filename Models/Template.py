from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TemplateModel(Base):
    __tablename__ = "templates"

    template_id = Column(Integer, primary_key=True, index=True)
    operation_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    active = Column(Integer, server_default=str(1))
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):
        self.operation_id = kwargs.get("operation_id")
        self.name = kwargs.get("name")
        self.content = kwargs.get("content")
        self.active = kwargs.get("active")
