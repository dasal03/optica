from sqlalchemy import select, insert, update
from Utils.ExceptionsTools import CustomException
from Utils.GeneralTools import get_input_data
from Utils.Validations import Validations
from Models.DocumentType import DocumentTypeModel


class DocumentType:
    """Class for manage document types."""

    def __init__(self, db):
        self.db = db
        self.validations = Validations(self.db)

    def get_document_types(self, event):
        """Get all active document types."""
        conditions = {"active": 1}

        stmt = select(DocumentTypeModel).filter_by(**conditions)

        results = self.db.query(stmt).as_dict()

        # Default value
        results.insert(
            0, {
                "document_type_id": 0,
                "description": "-- Seleccione una opción --"
            }
        )

        if results:
            status_code = 200
            data = results
        else:
            status_code = 404
            data = []

        return {"statusCode": status_code, "data": data}

    def create_document_type(self, event):
        request = get_input_data(event)
        description = request.get("description", "")

        validation_list = [
            self.validations.param("description", str, description)
        ]

        validated = self.validations.validate(validation_list, cast=True)

        if not validated["isValid"]:
            raise CustomException(validated["data"])

        stmt = insert(DocumentTypeModel).values(description=description)
        document_type_id = self.db.add(stmt)

        if document_type_id:
            status_code = 201
            data = {"document_type_id": document_type_id}
        else:
            status_code = 400
            data = "The document type couldn't be created. "
            "No properties changed"

        return {"statusCode": status_code, "data": data}

    def update_document_type(self, event):
        request = get_input_data(event)
        document_type_id = request.get("document_type_id", 0)
        description = request.get("description", "")

        self.validations.records(
            conn=self.db,
            model=DocumentTypeModel,
            pk=document_type_id,
            error_class=CustomException(
                "The provided document type does not exist"),
            as_dict=True
        )

        validation_list = [
            self.validations.param("description", str, description)
        ]

        validated = self.validations.validate(validation_list, cast=True)

        if not validated["isValid"]:
            raise CustomException(validated["data"])

        stmt = (
            update(DocumentTypeModel)
            .where(DocumentTypeModel.document_type_id == document_type_id)
            .values(description=description)
        )
        affected_rows = self.db.update(stmt)

        if affected_rows:
            status_code = 200
            data = "Document type updated successfully"
        else:
            status_code = 400
            data = "The document type couldn't be updated. "
            "No properties changed"

        return {"statusCode": status_code, "data": data}

    def delete_document_type(self, event):
        request = get_input_data(event)
        document_type_id = request.get("document_type_id", 0)

        self.validations.records(
            conn=self.db,
            model=DocumentTypeModel,
            pk=document_type_id,
            error_class=CustomException(
                "The provided document type does not exist"),
            as_dict=True
        )

        stmt = (
            update(DocumentTypeModel)
            .where(DocumentTypeModel.document_type_id == document_type_id)
            .values(active=0)
        )
        affected_rows = self.db.update(stmt)

        if affected_rows:
            status_code = 200
            data = "Document type deleted successfully"
        else:
            status_code = 400
            data = "The document type couldn't be deleted. "
            "No properties changed"

        return {"statusCode": status_code, "data": data}
