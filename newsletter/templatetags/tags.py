from django import template

register = template.Library()


@register.simple_tag
def active(path, url):
    if path.startswith(url):
        return "active"
    else:
        return ""
