from django import template
from django.utils.safestring import mark_safe

import markdown2

register = template.Library()


@register.filter('markdown_to_html')
def markdown_to_html(markdown_text):
    """
    Converts markdown text to HTML.
    """
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)


@register.simple_tag
def query_str(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)  # Remove or return 0 - aka, delete safely this key
    return updated.urlencode()

