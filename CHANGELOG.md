# Changelog

## 21.04

* The deprecated `sessions` parameter from user presence resource has been removed

## 21.02

* New read only parameters have been added to the user presence resource:

  * `connected`

* The following presence parameter has been deprecated:

  * `sessions`

## 20.11

* New read only parameters have been added to the user presence resource:

  * `do_not_disturb`

## 20.09

* Deprecate SSL configuration

## 19.10

* New query parameter has been added to the `GET /1.0/users/me/rooms/messages` endpoint:

  * `distinct`

## 19.09

* New state has been added to the `PUT /1.0./users/{user_uuid}/presence` endpoint:

  * `away`

* New read only parameters have been added to the user presence resource:

  * `last_activity`

* New query parameters have been added to the `GET /1.0/users/me/rooms/{room_uuid}/messages`
  endpoint:

  * `from_date`

## 19.07

* New query parameter have been added to the `GET /1.0./users/me/rooms/{room_uuid}/messages`
  endpoint:

  * `offset`
  * `search`

* New endpoints:
  * `GET /1.0/users/me/rooms/messages`

* New read only parameters have been added to the message resource:

  * `room_uuid`

## 19.05

* New endpoints:
  * `GET /1.0/users/me/rooms`
  * `POST /1.0/users/me/rooms`
  * `GET /1.0/users/me/rooms/{room_uuid}/messages`
  * `POST /1.0/users/me/rooms/{room_uuid}/messages`

## 19.03

* New endpoints:
  * `GET /1.0/users/presences`
  * `GET /1.0/users/{user_uuid}/presences`
  * `PUT /1.0/users/{user_uuid}/presences`

## 19.02

* New endpoints:
  * `GET /1.0/api/api.yml`
  * `GET /1.0/config`
  * `GET /1.0/status`
