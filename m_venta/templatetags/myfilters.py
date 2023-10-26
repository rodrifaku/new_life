from django import template

register = template.Library()


@register.filter
def intcomma(value):
    if value is None:
        return value
    return f'{value:,}'.replace(',', '.')
