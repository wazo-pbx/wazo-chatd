# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.chatd.events import (
    UserRoomCreatedEvent,
    UserRoomMessageCreatedEvent,
)

from .schemas import RoomSchema, MessageSchema


class RoomNotifier:
    def __init__(self, bus):
        self._bus = bus

    def created(self, room):
        room_json = RoomSchema().dump(room)
        for user in room_json['users']:
            event = UserRoomCreatedEvent(user['uuid'], room_json)
            self._bus.publish(
                event, headers={'user_uuid:{uuid}'.format(uuid=user['uuid']): True}
            )

    def message_created(self, room, message):
        message_json = MessageSchema().dump(message)
        for user in room.users:
            event = UserRoomMessageCreatedEvent(user.uuid, room.uuid, message_json)
            self._bus.publish(
                event, headers={'user_uuid:{uuid}'.format(uuid=user.uuid): True}
            )
