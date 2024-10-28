from django import template

register = template.Library()

@register.filter
def is_pdf(file_name):
    return file_name.endswith('.pdf')

