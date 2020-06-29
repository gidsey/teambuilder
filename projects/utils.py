from django.utils.text import slugify
from django.http import Http404


def get_slugified_list(queryset):
    """
    Return a sorted list of tuples containing the
    slugified and normal version of the given
    Queryset. Example of output:
    ('brand_new_app', 'Brand new app')
    """
    slugified_list = []
    for item in queryset:
        if (slugify(item), item) not in slugified_list:
            slugified_list.append((slugify(item), item))
    slugified_list.sort(key=lambda tup: tup[0].lower())
    return slugified_list


def get_project_needs(projects):
    """
    Return a sorted list of tuples containing the
    slugified and normal version of the Project Needs
    associated with the Projects QuerySet. e.g.
    ('project_needs', 'Project Needs')
    """
    project_needs = []
    for project in projects:
        for position in project.positions.all():
            if (slugify(position.title), position.title) not in project_needs:
                project_needs.append((slugify(position.title), position.title))
    project_needs.sort(key=lambda tup: tup[0].lower())
    return project_needs


def get_search_term(slug, queryset):
    """
    Return the de-slugified search term
    from the project_needs list(above)
    - if it exists, else return a 404.
    """
    try:
        search_term = [item[1] for item in queryset if slug in item][0]
    except IndexError:
        raise Http404
    return search_term
