from Utils.Response import Response
from Utils.ExceptionsTools import CustomException, get_and_print_error
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from DataBase.DataBase import DataBase


def authorized(func):
    """
    Decorator used as a middleware for lambda authorization
    :param func:
    :return:
    """

    def verify_authorization(event, context):

        try:
            conn = None
            data = {}

            conn = DataBase()

            event["user_id"] = 0
            data = func(event, context, conn)

            data["auth"] = True
        # EXCEPTIONS MANAGE
        # for customized exceptions with explicit message and overryding
        # the status code.
        except CustomException as err:
            data = get_and_print_error(err, err.status_code, err.message)

        # for asserts sentences not satisfied returning 412:
        # Precondition Failed and if not specified message in sentence
        # take generic400: "Missing or invalid params, check the
        # documentation of the API."
        except AssertionError as err:
            msg = str(err)
            data = get_and_print_error(err, 400, msg)

        # when error in key of dicts or try cast type or invalid in GET.
        # SECURITY: overryde error message with generic400.
        except (
            KeyError, ValueError, InvalidRequestError, AttributeError
        ) as err:
            msg = str(err)
            data = get_and_print_error(err, 400, msg)

        # when unappropied use of arg type
        # WARNIGNG: this exceptions return status code 5xx
        except TypeError as err:
            data = get_and_print_error(err, 500, str(err))

        # when raised db exceptions and general exception
        # WARNIGNG: this exceptions return status code 5xx
        except (SQLAlchemyError, Exception) as err:
            data = get_and_print_error(err, 500, str(err))

        # Formatting response
        r = Response(event, data, context)
        return r.getResponse()

    return verify_authorization


def response_format(func):
    """
    Decorator used for formatting response
    :param func:
    :return:
    """

    def response(event, context):
        data = func(event, context)
        # Formatting response
        return Response(event, data).getResponse(log=False)

    return response


def api_execution(func):
    """
    Decorator used as a middleware for api gateway authorization
    :param func:
    :return:
    """

    def wrapper(event, context, *args):
        return func(event, context, *args)

    return wrapper
