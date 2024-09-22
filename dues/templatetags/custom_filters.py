# dues/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    try:
        return field.as_widget(attrs={'class': css_class})
    except AttributeError:
        return field  # If field does not have as_widget method, return it unmodified
