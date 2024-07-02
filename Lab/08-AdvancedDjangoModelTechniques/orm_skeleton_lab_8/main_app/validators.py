from django.core.exceptions import ValidationError


def validate_menu_categories(value):
    for cat in ["Appetizers", "Main Course", "Desserts"]:
        if cat.lower() not in value.lower():
            raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')
