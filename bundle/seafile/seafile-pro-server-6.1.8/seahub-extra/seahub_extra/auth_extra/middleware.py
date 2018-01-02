# Copyright (c) 2012-2016 Seafile Ltd.
from .utils import populate_user_permissions


class UserPermissionMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return None

        populate_user_permissions(request.user)

        return None

    def process_response(self, request, response):
        return response
