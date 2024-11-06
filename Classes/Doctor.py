from sqlalchemy import select, insert, update, and_
from sqlalchemy.sql.functions import concat
from Utils.ExceptionsTools import CustomException
from Utils.GeneralTools import get_input_data
from Utils.Validations import Validations
from Models.Doctor import DoctorModel
from Models.DocumentType import DocumentTypeModel


class Doctor:
    """Class for manage doctors."""

    def __init__(self, db):
        self.db = db
        self.validations = Validations(self.db)

    def get_doctor_info(self, event):
        """Get user data from database."""
        request = get_input_data(event)
        conditions = {"active": 1}

        # Dinamic conditions
        if request:
            for key, value in request.items():
                conditions[key] = value

        stmt = (
            select(
                DoctorModel.doctor_id,
                concat(
                    DoctorModel.first_name, " ", DoctorModel.last_name
                ).label("full_name"),
                DoctorModel.email,
                DocumentTypeModel.description.label("document_type"),
                DoctorModel.document_type_id,
                DoctorModel.document_number,
                DoctorModel.date_of_birth,
                DoctorModel.created_at,
                DoctorModel.updated_at,
            )
            .filter_by(**conditions)
            .join(
                DocumentTypeModel,
                and_(
                    DoctorModel.document_type_id ==
                    DocumentTypeModel.document_type_id,
                    DocumentTypeModel.active == 1,
                ), isouter=True,
            )
        )
        response = self.db.query(stmt).as_dict()

        status_code = 200 if response else 404
        data = response if response else []

        return {"statusCode": status_code, "data": data}

    def register_doctor(self, event):
        """Get form data and create new user"""
        request = get_input_data(event)
        first_name = request.get("first_name", "")
        last_name = request.get("last_name", "")
        email = request.get("email", "")
        document_type_id = request.get("document_type_id", 0)
        document_number = request.get("document_number", 0)
        issuance_place = request.get("issuance_place", "")
        issuance_date = request.get("issuance_date", "")
        date_of_birth = request.get("date_of_birth", "")
        blood_type = request.get("blood_type", "")
        known_allergies = request.get("known_allergies", "")
        phone_number = request.get("phone_number", "")
        address = request.get("address", "")

        validated = self.validations.validate([
            self.validations.param("first_name", str, first_name),
            self.validations.param("last_name", str, last_name),
            self.validations.param("email", str, email),
            self.validations.param("document_type_id", int, document_type_id),
            self.validations.param("document_number", int, document_number),
            self.validations.param("issuance_place", str, issuance_place),
            self.validations.param("issuance_date", str, issuance_date),
            self.validations.param("date_of_birth", str, date_of_birth),
            self.validations.param("blood_type", str, blood_type),
            self.validations.param("known_allergies", str, known_allergies),
            self.validations.param("phone_number", str, phone_number),
            self.validations.param("address", str, address),
        ], cast=True)

        if not validated["isValid"]:
            raise CustomException(validated["data"])

        stmt = insert(DoctorModel).values(
            first_name=first_name,
            last_name=last_name,
            email=email,
            document_type_id=document_type_id,
            document_number=document_number,
            issuance_place=issuance_place,
            issuance_date=issuance_date,
            date_of_birth=date_of_birth,
            blood_type=blood_type,
            known_allergies=known_allergies,
            phone_number=phone_number,
            address=address
        )
        doctor_id = self.db.add(stmt)

        if doctor_id:
            status_code = 201
            data = {"doctor_id": doctor_id}
        else:
            status_code = 400
            data = {}

        return {"statusCode": status_code, "data": data}

    def update_doctor(self, event):
        """Receives user data and updates it in the database."""
        request = get_input_data(event)
        doctor_id = request.get("doctor_id", 0)

        self.validations.records(
            conn=self.db,
            model=DoctorModel,
            pk=doctor_id,
            error_class=CustomException("The provided user does not exist"),
            as_dict=True,
        )

        stmt = update(DoctorModel).where(
            DoctorModel.doctor_id == doctor_id
        ).values(**request)
        affected_rows = self.db.update(stmt)

        if affected_rows:
            status_code = 200
            data = "User updated successfully"
        else:
            status_code = 400
            data = "The user couldn't be updated. No properties changed"

        return {"statusCode": status_code, "data": data}

    def delete_doctor(self, event):
        request = get_input_data(event)
        doctor_id = request.get("doctor_id", 0)

        self.validations.records(
            conn=self.db,
            model=DoctorModel,
            pk=doctor_id,
            error_class=CustomException("The provided user does not exist"),
            as_dict=True,
        )

        stmt = update(DoctorModel).where(
            DoctorModel.doctor_id == doctor_id
        ).values(active=0)
        affected_rows = self.db.update(stmt)

        if affected_rows:
            status_code = 200
            data = "User deleted successfully"
        else:
            status_code = 400
            data = "The user couldn't be deleted. No properties changed"

        return {"statusCode": status_code, "data": data}
