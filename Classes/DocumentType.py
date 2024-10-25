from sqlalchemy import select
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

        stmt = select(
            DocumentTypeModel.document_type_id, DocumentTypeModel.description
        ).filter_by(**conditions)

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
        pass

    def update_document_type(self, event):
        pass

    def delete_document_type(self, event):
        pass
