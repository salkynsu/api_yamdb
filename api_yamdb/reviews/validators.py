from django.utils.timezone import now
from django.core.exceptions import ValidationError


def year_validator(value):
    if value > now().year:
        raise ValidationError("Год должен быть не больше текущего.")
    return value


def score_validator(value):
    if not (1 <= value <= 10):
        raise ValidationError("Оценка должна быть числом от 1 до 10.")
    return value
