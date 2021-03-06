from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MiddlewareNotUsed

# Put all permissions here
permission_params = (
    ('can_login', 'Can Login', 'auth', 'user'),
)

# Put all groups here, along with the names of the permissions you want the groups to have
groups = (
    ('Verified', ['can_login']),
)


def create_permission(perm_name, perm_desc, content_app, content_model):
    content_type = ContentType.objects.get(app_label=content_app, model=content_model)
    try:
        permission = Permission.objects.get(codename=perm_name, content_type=content_type)
    except Permission.DoesNotExist:
        permission = Permission.objects.create(name=perm_desc, codename=perm_name, content_type=content_type)

    return permission


def create_group(group_name, perms):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        group = Group.objects.create(name=group_name)

    group.permissions = perms
    group.save()

    return group


def populate_permissions():
    permissions = {}
    for name, desc, app, model in permission_params:
        permissions[name] = create_permission(name, desc, app, model)

    for group_name, perm_names in groups:
        group_perms = []
        for name in perm_names:
            group_perms.append(permissions[name])

        create_group(group_name, group_perms)




class PermissionInitMiddleware:

    def __init__(self):
        populate_permissions()
        raise MiddlewareNotUsed
