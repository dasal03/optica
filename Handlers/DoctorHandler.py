from Classes.Doctor import Doctor
from Utils.EventTools import authorized


@authorized
def doctor(event, context, conn):

    doctor_class = Doctor(conn)

    methods = {
        "GET": doctor_class.get_doctor_info,
        "POST": doctor_class.register_doctor,
        "PUT": doctor_class.update_doctor,
        "DELETE": doctor_class.delete_doctor,
    }

    method_to_be_executed = methods.get(event["httpMethod"])
    return method_to_be_executed(event)
