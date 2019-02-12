# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid

from functools import wraps

from wazo_chatd.database.models import (
    User,
    Session,
    Tenant,
)

from ..base import MASTER_TENANT_UUID


def user(**user_args):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            user_args.setdefault('uuid', str(uuid.uuid4()))
            user_args.setdefault('tenant_uuid', MASTER_TENANT_UUID)
            user_args.setdefault('state', 'unavailable')
            model = User(**user_args)

            user = self._user_dao.create(model)

            self._session.commit()
            args = list(args) + [user]
            try:
                result = decorated(self, *args, **kwargs)
            finally:
                self._session.expunge_all()
                self._session.query(User).filter(User.uuid == user_args['uuid']).delete()
                self._session.commit()
            return result
        return wrapper
    return decorator


def session(**session_args):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            session_args.setdefault('uuid', str(uuid.uuid4()))

            user_autogenerated = False
            if 'user_uuid' not in session_args:
                user_uuid = str(uuid.uuid4())
                model = User(uuid=user_uuid, tenant_uuid=MASTER_TENANT_UUID, state='available')
                self._user_dao.create(model)
                session_args['user_uuid'] = user_uuid
                user_autogenerated = True

            session = Session(**session_args)

            self._session.add(session)
            self._session.flush()

            self._session.commit()
            args = list(args) + [session]
            try:
                result = decorated(self, *args, **kwargs)
            finally:
                self._session.expunge_all()
                self._session.query(Session).filter(Session.uuid == session_args['uuid']).delete()
                if user_autogenerated:
                    self._session.query(User).filter(User.uuid == session_args['user_uuid']).delete()
                self._session.commit()
            return result
        return wrapper
    return decorator


def tenant(**tenant_args):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            tenant_args.setdefault('uuid', str(uuid.uuid4()))
            model = Tenant(**tenant_args)

            tenant = self._tenant_dao.create(model)

            self._session.commit()
            args = list(args) + [tenant]
            try:
                result = decorated(self, *args, **kwargs)
            finally:
                self._session.expunge_all()
                self._session.query(Tenant).filter(Tenant.uuid == tenant_args['uuid']).delete()
                self._session.commit()
            return result
        return wrapper
    return decorator