
def get_project_needs(projects):
    """
    Return a sorted list of Project Needs
    associated with the Projects QuerySet
    """
    project_needs = []
    for project in projects:
        for position in project.positions.all():
            if position.title not in project_needs:
                project_needs.append(position.title)
    project_needs = sorted(project_needs, key=str.casefold)
    return project_needs

