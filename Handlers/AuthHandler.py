from Classes.Auth import Auth
from Utils.EventTools import authorized


@authorized
def auth(event, context, conn):

    auth_class = Auth(conn)

    methods = {
        "POST": auth_class.login
    }

    # Select the method to be executed based on the user's petition.
    method_to_be_executed = methods.get(event["httpMethod"])
    return method_to_be_executed(event)
