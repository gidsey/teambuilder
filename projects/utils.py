from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.http import Http404

from . import models


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
    slugified_list[:0] = [('all', 'All Projects')]
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
    project_needs[:0] = [('all', 'All Needs')]
    return project_needs


def get_skill_choices(available_skills):
    """
    Get the skills choices to pass to the checkbox form
    :param available_skills:
    :return: a list of tuples (skill.id, skill.name)
    """
    choices = [(skill.id, skill.name) for skill in available_skills]
    choices.sort(key=lambda tup: tup[1].lower())  # Order the list by skill (case insensitive)
    return choices


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


def send_application_received_mail(email_to, name, position, project):
    """
    Send the application received email
    :param email_to: applicant's email
    :param name: applicant's name
    :param position: position applied for
    :param project: project associated with position
    :return: mail
    """
    mail = send_mail(
        'Team Builder application received',
        'Dear {}, \n\nThank you for applying for the position '
        'of {} on the {} project. \nWe will be back in touch with you shortly to let you know '
        'if your application has been successful.\n\nBest regards,\n'
        'From the team at Team Builder'.format(name, position, project),
        'admin@teambuilder.com',
        [email_to],
        fail_silently=False,
    )
    return mail


def send_application_result_mail(status, applicant, position_sought):
    """
    Send the application success or reject email
    :param status: accept or reject
    :param position_sought: position_id
    :param applicant: user_id
    :return: mail
    """
    try:
        application = models.UserApplication.objects.filter(
            user_id=applicant,
            position_id=position_sought
        ).prefetch_related('position', 'position__project', 'user__profile')
    except ObjectDoesNotExist:
        raise Http404

    for app in application:
        if status == 'accept':
            subject = 'Team Builder application successful'
            body = "Dear {}, \n\nThank you for your recent application for the position of {} on the {} project. \n" \
                   "We are delighted to inform you that your application has been successful.\n\n" \
                   "Welcome to the team!\n\nBest regards,\nFrom the team at " \
                   "Team Builder".format(app.user.profile.fullname, app.position, app.position.project)
        elif status == 'reject':
            subject = 'Team Builder application unsuccessful'
            body = "Dear {}, \n\nThank you for your recent application for the position of {} on the {} project. \n" \
                   "We are sorry to inform you that on this occasion your application has not been successful.\n\n" \
                   "Better luck next time!\n\nBest regards,\nFrom the team at " \
                   "Team Builder".format(app.user.profile.fullname, app.position, app.position.project)

    from_adr = 'admin@teambuilder.com'
    mail = send_mail(
        subject,
        body,
        from_adr,
        [app.user.email],
        fail_silently=False,
    )
    return mail


def get_skill_sets(form, pk):
    # form_true = the skills that need to set to true for the current project
    form_true = [int(skill) for skill in form.cleaned_data['project_skills']]

    # Create 2 sets (form_true and db_skills):
    form_true = set(form_true)
    # db_skills = all the skills associated with the current project (set either true or false)
    db_skills = set([skill.skill_id for skill in models.ProjectSkill.objects.filter(project_id=pk)])

    # Use the sets to define which skills should be set to True and which to False
    set_to_false = db_skills - form_true
    set_to_true = form_true - set_to_false

    return set_to_false, set_to_true
