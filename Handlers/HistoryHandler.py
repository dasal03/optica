from Classes.History import History
from Utils.EventTools import authorized


@authorized
def history(event, context, conn):

    history_class = History(conn)

    methods = {
        "GET": history_class.search_history,
        "POST": history_class.create_history,
        "PUT": history_class.update_history,
        "DELETE": history_class.delete_history
    }

    # Select the method to be executed based on the user's petition.
    method_to_be_executed = methods.get(event["httpMethod"])
    return method_to_be_executed(event)
