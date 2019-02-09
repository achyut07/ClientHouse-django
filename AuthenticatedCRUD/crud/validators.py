from django.core import validators


class UsernameValidator(validators.RegexValidator):
    regex = r'^[\w.-]+$'
    message = 'Enter a valid username. This value may contain only letters, numbers, and ./-/_characters.'

# class PhoneNumberValidator(validators.RegexValidator):
#     regex = r'^\+?1?\d{9,15}$'
#     message = 'Enter a valid Phone number.'
