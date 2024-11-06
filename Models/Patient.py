from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PatientModel(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    document_type_id = Column(Integer, nullable=False)
    document_number = Column(Integer, nullable=False)
    issuance_place = Column(String(255), nullable=False)
    issuance_date = Column(Date, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    blood_type = Column(String(255), nullable=False)
    known_allergies = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    active = Column(Integer, server_default=str(1))
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.email = kwargs.get("email")
        self.document_type_id = kwargs.get("document_type_id")
        self.document_number = kwargs.get("document_number")
        self.issuance_place = kwargs.get("issuance_place")
        self.issuance_date = kwargs.get("issuance_date")
        self.date_of_birth = kwargs.get("date_of_birth")
        self.blood_type = kwargs.get("blood_type")
        self.known_allergies = kwargs.get("known_allergies")
        self.phone_number = kwargs.get("phone_number")
        self.address = kwargs.get("address")
