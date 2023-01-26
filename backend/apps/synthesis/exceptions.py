from rest_framework.exceptions import APIException


class SynthesisNotFound(APIException):
    status_code = 404
    default_detail = "The requested property doest not exists"

