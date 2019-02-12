# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.mallow import fields
from xivo.mallow.validate import (
    OneOf,
)
from xivo.mallow_helpers import Schema


class SessionPresenceSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    mobile = fields.Boolean(dump_only=True)


class UserPresenceSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    tenant_uuid = fields.UUID(dump_only=True)

    state = fields.String(
        required=True,
        validate=OneOf(['available', 'unavailable', 'invisible']),
    )
    status = fields.String(allow_none=True)
    sessions = fields.Nested(
        'SessionPresenceSchema',
        many=True,
        dump_only=True
    )


class ListRequestSchema(Schema):

    recurse = fields.Boolean(missing=False)