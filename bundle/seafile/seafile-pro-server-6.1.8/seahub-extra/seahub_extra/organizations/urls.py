# Copyright (c) 2012-2016 Seafile Ltd.
from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^add/$', org_add, name='org_add'),
    url(r'^register/$', org_register, name='org_register'),

    url(r'^useradmin/$', org_user_admin, name='org_user_admin'),
    url(r'^useradmin/admins/$', org_useradmin_admins, name='org_useradmin_admins'),
    url(r'^useradmin/add/$', org_user_add, name="org_user_add"),
    url(r'^useradmin/remove/(?P<user_id>\d+)/$', org_user_remove, name="org_user_remove"),
    url(r'^useradmin/search/$', org_user_search, name="org_user_search"),
    url(r'^useradmin/password/reset/(?P<user_id>\d+)/$', org_user_reset, name='org_user_reset'),
    url(r'^useradmin/makeadmin/(?P<user_id>\d+)/$', org_user_make_admin, name='org_user_make_admin'),
    url(r'^useradmin/batchmakeadmin/$', batch_org_user_make_admin, name='batch_org_user_make_admin'),
    url(r'^useradmin/removeadmin/(?P<user_id>\d+)/$', org_user_remove_admin, name='org_user_remove_admin'),
    url(r'^useradmin/info/(?P<email>[^/]+)/$', org_user_info, name='org_user_info'),
    url(r'^useradmin/toggle_status/(?P<user_id>[^/]+)/$', org_user_toggle_status, name='org_user_toggle_status'),
    url(r'^useradmin/(?P<email>[^/]+)/set_quota/$', org_user_set_quota, name='org_user_set_quota'),
    url(r'^repoadmin/$', org_repo_admin, name='org_repo_admin'),
    url(r'^repoadmin/transfer/$', org_repo_transfer, name='org_repo_transfer'),
    url(r'^repoadmin/delete/(?P<repo_id>[-0-9a-f]{36})/$', org_repo_delete, name='org_repo_delete'),

    url(r'^repoadmin/search/$$', org_repo_search, name='org_repo_search'),
    url(r'^groupadmin/$', org_group_admin, name='org_group_admin'),
    url(r'^groupadmin/(?P<group_id>\d+)/$', org_admin_group_info, name='org_admin_group_info'),
    url(r'^groupadmin/remove/(?P<group_id>\d+)/$', org_group_remove, name='org_group_remove'),
    url(r'^publinkadmin/$', org_publink_admin, name='org_publink_admin'),
    url(r'^publinkadmin/remove/$', org_publink_remove, name='org_publink_remove'),
    url(r'^file-audit-admin/$', org_log_file_audit, name='org_log_file_audit'),
    url(r'^file-update-admin/$', org_log_file_update, name='org_log_file_update'),
    url(r'^perm-audit-admin/$', org_log_perm_audit, name='org_log_perm_audit'),

    url(r'^orgmanage/$', org_manage, name='org_manage'),

)
