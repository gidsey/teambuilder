from . import models


def user_directory_path(instance, filename):
    """Get the user directory path"""
    # file will be uploaded to MEDIA_ROOT/avatars/user/<filename>
    return 'avatars/{0}/{1}'.format(instance.user, filename)


def get_skill_sets(request, form, formset):
    """
    Define which skills should be set to True and which to False.
    """

    # form_true = the skills that need to set to true for the current user
    form_true = [int(skill) for skill in form.cleaned_data['skills']]

    #  Create a list of custom skills added by the user
    custom_skill_list = []
    for custom_skill_form in formset:
        skill = custom_skill_form.cleaned_data.get('name')
        if skill:  # prevent 'None' being saved to list
            custom_skill_list.append(skill)

    #  Add the custom skills to the Skills model (if they don't already exist)
    for custom_skill in custom_skill_list:
        obj, created = models.Skill.objects.get_or_create(
            name=custom_skill,
            type='c'
        )
        form_true.append(obj.id)  # Append the new custom skills to the form_true list

    # Create 2 sets (form_true and db_skills):
    form_true = set(form_true)

    # db_skills = all the skills associated with the current user (set either true or false)
    db_skills = set([skill.skill_id for skill in models.UserSkill.objects.filter(user_id=request.user.id)])

    set_to_false = db_skills - form_true
    set_to_true = form_true - set_to_false

    return set_to_false, set_to_true





