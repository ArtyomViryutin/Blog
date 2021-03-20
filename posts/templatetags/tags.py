from django import template
from posts.models import Follow
register = template.Library()


@register.simple_tag
def is_subscribed(user, author):
    return Follow.objects.filter(user=user, author=author).exists()
