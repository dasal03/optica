from Classes.DocumentType import DocumentType
from Utils.EventTools import authorized


@authorized
def document_type(event, context, conn):

    doc_type_class = DocumentType(conn)

    methods = {
        "GET": doc_type_class.get_document_types,
        "POST": doc_type_class.create_document_type,
        "PUT": doc_type_class.update_document_type,
        "DELETE": doc_type_class.delete_document_type,
    }

    # Select the method to be executed based on the user's petition.
    method_to_be_executed = methods.get(event["httpMethod"])
    return method_to_be_executed(event)
