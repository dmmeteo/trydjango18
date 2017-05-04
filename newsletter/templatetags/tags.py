from django import template

register = template.Library()


@register.simple_tag
def active(path, url):
    print url
    if path.startswith(url):
        return "active"
    else:
        return ""
