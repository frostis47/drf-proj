from django.core.exceptions import ValidationError

def validate_youtube_link(value):
    if value and "youtube.com" not in value:
        raise ValidationError("Разрешены только ссылки на youtube.com")
