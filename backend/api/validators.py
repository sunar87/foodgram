from rest_framework.exceptions import ValidationError
from users.models import Subscriptions


def validate_no_self_subscription(user, author):
    if user == author:
        raise ValidationError('Нельзя подписаться на самого себя')


def validate_unique_subscription(user, author):
    if Subscriptions.objects.filter(user=user, author=author).exists():
        raise ValidationError('Нельзя подписаться на автора дважды')
