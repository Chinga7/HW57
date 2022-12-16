from django.forms import ValidationError


def not_only_numeric(string):
    if string.isdigit():
        raise ValidationError('It must contain character symbols')