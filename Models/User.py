from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    document_type_id = Column(Integer, nullable=False)
    document_number = Column(Integer, nullable=False)
    birthdate = Column(Date, nullable=False)
    role_id = Column(Integer, nullable=False)
    profile_picture = Column(String(255), nullable=True)
    active = Column(Integer, server_default=str(1))
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime, default=current_timestamp(), onupdate=current_timestamp()
    )

    def __init__(self, **kwargs):
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.email = kwargs.get("email")
        self.document_type_id = kwargs.get("document_type_id")
        self.document_number = kwargs.get("document_number")
        self.birthdate = kwargs.get("birthdate")
        self.role_id = kwargs.get("role_id")
        self.profile_picture = kwargs.get("profile_picture")
