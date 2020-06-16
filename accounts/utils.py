

def machine_name(label):
    """
    Remove white space and upper case characters from string input.
    """
    return label.lower().replace(' ', '_')


def user_directory_path(instance, filename):
    """Get the user directory path"""
    # file will be uploaded to MEDIA_ROOT/avatars/user/<filename>
    return 'avatars/{0}/{1}'.format(instance.user, filename)