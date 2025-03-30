from django import template
from events.models import Event

register = template.Library()

@register.filter
def status_display(code):
    """Преобразует код статуса в читаемое название"""
    return dict(Event.STATUS_CHOICES).get(code, code)