from rest_framework.response import Response


def response_handler(function):
    def wrapper(*args, **kwargs):
        try:
            res = function(*args, **kwargs)
            return res
        except Exception as e:
            print(e)
            return Response({"message":"An error occurred"}, status=500)

    return wrapper
