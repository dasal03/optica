from datetime import datetime
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MedicalHistoryModel(Base):
    __tablename__ = "medical_histories"
    medical_history_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False)
    consultation_date = Column(DateTime, default=datetime.utcnow)
    visit_reason = Column(Text, nullable=True)
    visual_acuity_re = Column(String(50), nullable=True)
    visual_acuity_le = Column(String(50), nullable=True)
    near_vision_re = Column(String(50), nullable=True)
    near_vision_le = Column(String(50), nullable=True)
    distance_vision_re = Column(String(50), nullable=True)
    distance_vision_le = Column(String(50), nullable=True)
    past_medical_conditions = Column(Text, nullable=True)
    current_medication = Column(Text, nullable=True)
    fundus_exam = Column(Text, nullable=True)
    intraocular_pressure_re = Column(String(50), nullable=True)
    intraocular_pressure_le = Column(String(50), nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    additional_notes = Column(Text, nullable=True)
    active = Column(Integer, server_default=str(1))
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):
        self.patient_id = kwargs.get("patient_id")
        self.consultation_date = kwargs.get("consultation_date")
        self.visit_reason = kwargs.get("visit_reason")
        self.visual_acuity_re = kwargs.get("visual_acuity_re")
        self.visual_acuity_le = kwargs.get("visual_acuity_le")
        self.near_vision_re = kwargs.get("near_vision_re")
        self.near_vision_le = kwargs.get("near_vision_le")
        self.distance_vision_re = kwargs.get("distance_vision_re")
        self.distance_vision_le = kwargs.get("distance_vision_le")
        self.past_medical_conditions = kwargs.get("past_medical_conditions")
        self.current_medication = kwargs.get("current_medication")
        self.fundus_exam = kwargs.get("fundus_exam")
        self.intraocular_pressure_re = kwargs.get("intraocular_pressure_re")
        self.intraocular_pressure_le = kwargs.get("intraocular_pressure_le")
        self.diagnosis = kwargs.get("diagnosis")
        self.treatment_plan = kwargs.get("treatment_plan")
        self.additional_notes = kwargs.get("additional_notes")
