from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ConsultationModel(Base):
    __tablename__ = "consultations"

    consultation_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    visual_acuity_re = Column(String(50), nullable=True)
    visual_acuity_le = Column(String(50), nullable=True)
    near_vision_re = Column(String(50), nullable=True)
    near_vision_le = Column(String(50), nullable=True)
    distance_vision_re = Column(String(50), nullable=True)
    distance_vision_le = Column(String(50), nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    additional_notes = Column(Text, nullable=True)
    active = Column(Integer, server_default="1")
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):
        self.patient_id = kwargs.get("patient_id")
        self.doctor_id = kwargs.get("doctor_id")
        self.reason = kwargs.get("reason")
        self.visual_acuity_re = kwargs.get("visual_acuity_re")
        self.visual_acuity_le = kwargs.get("visual_acuity_le")
        self.near_vision_re = kwargs.get("near_vision_re")
        self.near_vision_le = kwargs.get("near_vision_le")
        self.distance_vision_re = kwargs.get("distance_vision_re")
        self.distance_vision_le = kwargs.get("distance_vision_le")
        self.diagnosis = kwargs.get("diagnosis")
        self.treatment_plan = kwargs.get("treatment_plan")
        self.additional_notes = kwargs.get("additional_notes")
