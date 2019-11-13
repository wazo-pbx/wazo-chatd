# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import datetime
import string
import random
import uuid

from functools import wraps

from wazo_chatd.database.models import (
    Endpoint,
    Line,
    Room,
    RoomMessage,
    RoomUser,
    Session,
    RefreshToken,
    Tenant,
    User,
)

from ..base import TOKEN_TENANT_UUID, WAZO_UUID


def user(**user_args):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            user_args.setdefault('uuid', str(uuid.uuid4()))
            user_args.setdefault('tenant_uuid', TOKEN_TENANT_UUID)
            user_args.setdefault('state', 'unavailable')
            model = User(**user_args)

            user = self._dao.user.create(model)

            self._session.commit()
            args = list(args) + [user]
            try:
                result = decorated(self, *args, **kwargs)
            finally:
                self._session.expunge_all()
                self._session.query(User).filter(
                    User.uuid == user_args['uuid']
                ).delete()
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
                model = User(
                    uuid=user_uuid, tenant_uuid=TOKEN_TENANT_UUID, state='available'
                )
                self._dao.user.create(model)
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
                self._session.query(Session).filter(
                    Session.uuid == session_args['uuid']
                ).delete()
                if user_autogenerated:
                    self._session.query(User).filter(
                        User.uuid == session_args['user_uuid']
                    ).delete()
                self._session.commit()
            return result

        return wrapper

    return decorator


def refresh_token(**refresh_token_args):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            refresh_token_args.setdefault('client_id', _random_string())

            user_autogenerated = False
            if 'user_uuid' not in refresh_token_args:
                user_uuid = str(uuid.uuid4())
                model = User(
                    uuid=user_uuid, tenant_uuid=TOKEN_TENANT_UUID, state='available'
                )
                self._dao.user.create(model)
                refresh_token_args['user_uuid'] = user_uuid
                user_autogenerated = True

            refresh_token = RefreshToken(**refresh_token_args)

            self._session.add(refresh_token)
            self._session.flush()

            self._session.commit()
            args = list(args) + [refresh_token]
            try:
                result = decorated(self, *args, **kwargs)
            finally:
                self._session.expunge_all()
                self._session.query(RefreshToken).filter(
                    RefreshToken.client_id == refresh_token_args['client_id']
                ).delete()
                if user_autogenerated:
                    self._session.query(User).filter(
                        User.uuid == refresh_token_args['user_uuid']
                    ).delete()
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

            tenant = self._dao.tenant.create(model)

            self._session.commit()
            args = list(args) + [tenant]
            try:
                result = decorated(self, *args, **kwargs)
            finally:
                self._session.expunge_all()
                self._session.query(Tenant).filter(
                    Tenant.uuid == tenant_args['uuid']
                ).delete()
                self._session.commit()
            return result

        return wrapper

    return decorator


def line(**line_args):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            line_args.setdefault('id', random.randint(1, 1000000))

            user_autogenerated = False
            if 'user_uuid' not in line_args:
                user_uuid = str(uuid.uuid4())
                model = User(
                    uuid=user_uuid, tenant_uuid=TOKEN_TENANT_UUID, state='available'
                )
                self._dao.user.create(model)
                line_args['user_uuid'] = user_uuid
                user_autogenerated = True

            line = Line(**line_args)

            self._session.add(line)
            self._session.flush()

            self._session.commit()
            args = list(args) + [line]
            try:
                result = decorated(self, *args, **kwargs)
            finally:
                self._session.expunge_all()
                self._session.query(Line).filter(Line.id == line_args['id']).delete()
                if user_autogenerated:
                    self._session.query(User).filter(
                        User.uuid == line_args['user_uuid']
                    ).delete()
                self._session.commit()
            return result

        return wrapper

    return decorator


def room(**room_args):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            room_args.setdefault('uuid', str(uuid.uuid4()))
            room_args.setdefault('tenant_uuid', TOKEN_TENANT_UUID)
            room_args.setdefault('users', [])
            room_args.setdefault('messages', [])

            for user_args in room_args['users']:
                user_args.setdefault('uuid', str(uuid.uuid4()))
                user_args.setdefault('tenant_uuid', room_args['tenant_uuid'])
                user_args.setdefault('wazo_uuid', WAZO_UUID)

            now = datetime.datetime.utcnow()
            for i, message_args in enumerate(room_args['messages']):
                created_at = now + datetime.timedelta(seconds=i)
                message_args.setdefault('user_uuid', str(uuid.uuid4()))
                message_args.setdefault('tenant_uuid', room_args['tenant_uuid'])
                message_args.setdefault('wazo_uuid', WAZO_UUID)
                message_args.setdefault('created_at', created_at)

            room_args['users'] = [
                RoomUser(**user_args) for user_args in room_args['users']
            ]
            room_args['messages'] = [
                RoomMessage(**msg_args) for msg_args in room_args['messages']
            ]
            room = Room(**room_args)

            self._session.add(room)
            self._session.flush()

            self._session.commit()
            args = list(args) + [room]
            try:
                result = decorated(self, *args, **kwargs)
            finally:
                self._session.expunge_all()
                self._session.query(Room).filter(
                    Room.uuid == room_args['uuid']
                ).delete()
                self._session.commit()
            return result

        return wrapper

    return decorator


def endpoint(**endpoint_args):
    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            endpoint_args.setdefault('name', _random_endpoint_name())
            endpoint_args.setdefault('state', 'unavailable')

            endpoint = Endpoint(**endpoint_args)

            self._session.add(endpoint)
            self._session.flush()

            self._session.commit()
            args = list(args) + [endpoint]
            try:
                result = decorated(self, *args, **kwargs)
            finally:
                self._session.expunge_all()
                self._session.query(Endpoint).filter(
                    Endpoint.name == endpoint_args['name']
                ).delete()
                self._session.commit()
            return result

        return wrapper

    return decorator


def _random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def _random_endpoint_name(length=10):
    return 'SIP/{}'.format(_random_string(length))
