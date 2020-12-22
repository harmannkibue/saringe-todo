
import re
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.utils.deconstruct import deconstructible
from django.db import models


@deconstructible()
class CustomPhoneValidator:
    message = "Enter a valid phone number"
    code = "invalid"

    valid_characters = re.compile(r"^\+\d{12}|\d{12}|0\d{9}")

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, phone):

        valid_phone = re.match(self.valid_characters, phone)

        if not valid_phone:
            raise ValidationError(self.message, code=self.code)
        # else:
        #     phone = phone.strip('+')
        #     if phone[0] == "0":
        #         phone = "254" + phone[1:]
        #         return phone
        #     else:
        #         return phone

    def __eq__(self, other):
        return (
                isinstance(other, CustomPhoneValidator) and
                (self.message == other.message) and
                (self.code == other.code)
        )


class CustomPhoneSerializer(serializers.CharField):
    default_error_messages = {
        "invalid": "Enter a valid phone number"
    }

    def __init__(self, **kwargs):
        kwargs['max_length'] = 14
        super().__init__(**kwargs)
        validator = CustomPhoneValidator(message=self.error_messages['invalid'])
        self.validators.append(validator)


class CustomPhoneField(models.CharField):
    default_error_messages = {
        "invalid": "Enter a valid phone number"
    }

    def __init__(self, **kwargs):
        kwargs['max_length'] = 14
        super().__init__(**kwargs)
        validator = CustomPhoneValidator(message=self.error_messages['invalid'])
        self.validators.append(validator)
