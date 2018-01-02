# Copyright (c) 2012-2016 Seafile Ltd.
import os

# haiwen/
# |___seafile-pro-server-1.7.0/
#         |____ seahub
#             |____ seahub/
#                  |____ setings.py
#         |____ seahub-extra
#             |____ seahub_extra/
#                  |____ seahub_extra_settings.py (this file)
# |___pro-data
#    |___ search index
# |___ccnet/
# |___seafile-data/
# |___conf/
#    |___ seafevents.conf

d = os.path.dirname

topdir = d(d(d(d(os.path.abspath(__file__)))))

EVENTS_CONFIG_FILE = os.environ.get('EVENTS_CONFIG_FILE',
    os.path.join(topdir, 'conf', 'seafevents.conf'))


if not os.path.exists(EVENTS_CONFIG_FILE):
    del EVENTS_CONFIG_FILE

del d, topdir

EXTRA_INSTALLED_APPS = (
    "seahub_extra.search",
    "seahub_extra.sysadmin_extra",
    'seahub_extra.organizations',
    'seahub_extra.auth_extra',
    'seahub_extra.krb5_auth',
    "seahub_extra.two_factor",
)

EXTRA_MIDDLEWARE_CLASSES = (
    'seahub_extra.two_factor.middleware.OTPMiddleware',
    'seahub_extra.organizations.middleware.RedirectMiddleware',
    # No need for this middleware, ref: https://github.com/haiwen/seahub/commit/26200028981623c315c2b0a6282380e3cb80653f
    # 'seahub_extra.auth_extra.middleware.UserPermissionMiddleware',
)

USE_PDFJS = False

ENABLE_SYSADMIN_EXTRA = True

MULTI_TENANCY = False

ENABLE_UPLOAD_FOLDER = True

ENABLE_FOLDER_PERM = True
