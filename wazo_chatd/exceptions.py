# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.rest_api_helpers import APIException


class UnknownUserException(APIException):

    def __init__(self, user_uuid):
        msg = 'No such user: "{}"'.format(user_uuid)
        details = {'uuid': str(user_uuid)}
        super().__init__(404, msg, 'unknown-user', details, 'users')


class UnknownUsersException(APIException):

    def __init__(self, user_uuids):
        msg = 'No such users: {}'.format(
            ', '.join(map(lambda uuid: '"{}"'.format(uuid), user_uuids)),
        )
        details = {'uuids': user_uuids}
        super().__init__(404, msg, 'unknown-users', details, 'users')


class UnknownTenantException(APIException):

    def __init__(self, tenant_uuid):
        msg = 'No such tenant: "{}"'.format(tenant_uuid)
        details = {'uuid': str(tenant_uuid)}
        super().__init__(404, msg, 'unknown-tenant', details, 'tenants')


class UnknownSessionException(APIException):

    def __init__(self, session_uuid):
        msg = 'No such session: "{}"'.format(session_uuid)
        details = {'uuid': str(session_uuid)}
        super().__init__(404, msg, 'unknown-session', details, 'sessions')