from django import template

register = template.Library()

@register.filter(name='not_in_list')
def not_in_list(value, arg):
    return value not in arg.split(',')