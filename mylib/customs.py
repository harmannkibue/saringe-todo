from rest_framework.exceptions import APIException
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf.global_settings import DEFAULT_FROM_EMAIL
import string
import random
from rest_framework.pagination import PageNumberPagination


class MyCustomException(APIException):
    status_code = 503
    detail = "Service temporarily unavailable, try again later."
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

    def __init__(self, message, code=400):
        self.status_code = code
        self.default_detail = message
        self.detail = message


def code_generator(length=6):
    letters_and_digits = string.ascii_lowercase + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))

    return result_str


def email_send(subject, template, data, recipients, from_email=None):
    if from_email is None:
        from_email = DEFAULT_FROM_EMAIL
    rendered = render_to_string(template, data)
    # print("Sending email...")
    email = send_mail(
        subject=subject,
        message="",
        html_message=rendered,
        from_email=from_email,
        recipient_list=recipients,
        fail_silently=False,
    )
    return email


class AdminResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50


def filestream_parser(request):
    path = request.path.replace("/m/", "")
    unique_code = path[:6]
    file_name = path[6:]
    # print("The uniqeu file_name", unique_code, file_name)
    return unique_code, file_name
