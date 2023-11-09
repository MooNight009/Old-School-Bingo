import re

from django.core.exceptions import ValidationError


def validate_string_special_free(value):
    regex = r"^[\w\s. @ +, \-()!]+$"
    if not re.match(regex, value):
        raise ValidationError(
            "This field may only contain letters, numbers, and the characters '@', '.', '+', '-', or '_'"
        )


def validate_name_list(value):
    regex = r"^[\w, -]+\Z"
    if len(value)!= 0 and not re.match(regex, value):
        raise ValidationError(
            "This field may only contain letters, numbers, space, and '-'"
        )


def check_string_special_free(value):
    regex = r"^[\w.@+ -]+\Z"
    return re.match(regex, value)


def validate_discord_link(value):
    regex = r"^[A-Za-z0-9:/-]+$"
    if not re.match(regex, value):
        print("Going to raise validation for discord link")
        raise ValidationError(
            "This field may only contain letters, numbers, and the characters ':', '/', and '-'"
        )
