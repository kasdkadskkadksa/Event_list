from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """Обновляет GET-параметры с возможностью удаления через None."""
    request = context["request"]
    params = request.GET.copy()
    for key, value in kwargs.items():
        if value is None:
            if key in params:
                del params[key]
        else:
            params[key] = value
    return params.urlencode()

@register.simple_tag(takes_context=True)
def sort_url(context, field_name):
    """Генерирует URL для сортировки."""
    request = context["request"]
    params = request.GET.copy()
    current_sort = params.get("sort", "")

    if current_sort.lstrip("-") == field_name:
        new_sort = f"-{field_name}" if not current_sort.startswith("-") else field_name
    else:
        new_sort = field_name

    params["sort"] = new_sort
    return params.urlencode()