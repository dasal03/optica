from sqlalchemy import select
from Models.DocumentType import DocumentTypeModel


class DocumentType:
    """Class for manage document types."""
    def __init__(self, db):
        self.db = db

    def get_document_types(self):
        """Get all active document types."""
        stmt = select(
            DocumentTypeModel.document_type_id,
            DocumentTypeModel.description
        ).where(DocumentTypeModel.active == 1)
        results = self.db.query(stmt).as_dict()

        if not results:
            # Default value
            results = [{
                "document_type_id": 0,
                "description": "-- Seleccione una opción --"
            }]

        results.insert(
            0, {
                "document_type_id": 0,
                "description": "-- Seleccione una opción --"
            }
        )

        return results
