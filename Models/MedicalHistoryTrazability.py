from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MedicalHistoryTrazabilityModel(Base):
    __tablename__ = "medical_histories_trazability"
    medical_history_trazability_id = Column(
        Integer, primary_key=True, index=True)
    medical_history_id = Column(Integer, nullable=False)
    file_url = Column(String(255), nullable=False)
    active = Column(Integer, server_default=str(1))
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):
        self.medical_history_id = kwargs.get("medical_history_id")
        self.file_url = kwargs.get("file_url")
