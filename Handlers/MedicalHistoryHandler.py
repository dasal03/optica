from Classes.MedicalHistory import MedicalHistory
from Utils.EventTools import authorized


@authorized
def medical_history(event, context, conn):

    history_class = MedicalHistory(conn)

    methods = {
        "GET": history_class.get_medical_history,
        "POST": history_class.generate_medical_history_pdf,
    }

    method_to_be_executed = methods.get(event["httpMethod"])
    return method_to_be_executed(event)
