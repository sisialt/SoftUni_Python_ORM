from django.core.exceptions import ValidationError


def validate_name(value):
    for ch in value:
        if not (ch.isalpha() or ch == " "):
            raise ValidationError("Name can only contain letters and spaces")


def validate_phone_number(value):
    # if not re.match(r'^\+359\d{9}$', value):
    if not (value[:4] == "+359" and len(value) == 13 and value[1::].isdigit()):
        raise ValidationError("Phone number must start with a '+359' followed by 9 digits")
