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


@register.filter('order_by')
def order_by(queryset, args):
    """
    Sort the queryset by supplied arg
    """
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)


@register.simple_tag
def query_str(request, **kwargs):
    """
    Return urlencoded query strings.
    """
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)  # Remove or return 0 - aka, delete safely this key
    return updated.urlencode()


@register.filter('check_application_status')
def check_application_status(applications, user):
    """
    Loop through each application and compile a list of applicants.
    Check the current user and return True if they are in that list:
    i.e. they have already applied for the position.
    """
    applicants = [app.user for app in applications]
    if user in applicants:
        return True
