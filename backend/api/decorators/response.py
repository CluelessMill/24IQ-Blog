from icecream import ic
from rest_framework.response import Response


def response_handler(function):
    def wrapper(*args, **kwargs):
        try:
            res = function(*args, **kwargs)
            return res
        except Exception as e:
            ic(e, function)
            return Response({"message": "An error occured"}, status=500)

    return wrapper
