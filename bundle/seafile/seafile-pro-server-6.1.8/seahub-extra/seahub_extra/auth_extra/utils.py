# Copyright (c) 2012-2016 Seafile Ltd.
from seahub.constants import DEFAULT_USER
from seahub.role_permissions.utils import get_enabled_role_permissions_by_role

def populate_user_permissions(user):
    user_role = DEFAULT_USER if user.role is None else user.role
    if user_role == DEFAULT_USER:
        # no need to populate permissions to 'deafult' user, since they are
        # already set in seahub/base/accounts.py::UserPermissions
        return

    user.permissions.can_add_repo = lambda: get_enabled_role_permissions_by_role(user_role)['can_add_repo']
    user.permissions.can_generate_share_link = lambda: get_enabled_role_permissions_by_role(user_role)['can_generate_share_link']
    user.permissions.can_generate_upload_link = lambda: get_enabled_role_permissions_by_role(user_role)['can_generate_upload_link']
    user.permissions.can_view_org = lambda: get_enabled_role_permissions_by_role(user_role)['can_view_org']
    user.permissions.can_use_global_address_book = lambda: get_enabled_role_permissions_by_role(user_role)['can_use_global_address_book']
    user.permissions.can_add_group = lambda: get_enabled_role_permissions_by_role(user_role)['can_add_group']
    user.permissions.can_invite_guest = lambda: get_enabled_role_permissions_by_role(user_role)['can_invite_guest']
    user.permissions.role_quota = lambda: get_enabled_role_permissions_by_role(user_role).get('role_quota', '')

    user.permissions.can_connect_with_android_clients = lambda: get_enabled_role_permissions_by_role(user_role)['can_connect_with_android_clients']
    user.permissions.can_connect_with_ios_clients = lambda: get_enabled_role_permissions_by_role(user_role)['can_connect_with_ios_clients']
    user.permissions.can_connect_with_desktop_clients = lambda: get_enabled_role_permissions_by_role(user_role)['can_connect_with_desktop_clients']
    user.permissions.can_export_files_via_mobile_client = lambda: get_enabled_role_permissions_by_role(user_role)['can_export_files_via_mobile_client']
    user.permissions.can_drag_drop_folder_to_sync = lambda: get_enabled_role_permissions_by_role(user_role)['can_drag_drop_folder_to_sync']
