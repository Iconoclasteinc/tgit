# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import json
from concurrent.futures import ThreadPoolExecutor

from requests import get, post

from tgit.promise import Promise


class AuthenticationError(Exception):
    pass


class InsufficientInformationError(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


class PlatformConnectionError(Exception):
    pass


def _check_response_code(response):
    if response.status_code == 401:
        raise AuthenticationError()
    if response.status_code == 402:
        raise PermissionDeniedError()
    if response.status_code == 422:
        raise InsufficientInformationError()
    if response.status_code >= 500:
        raise PlatformConnectionError()


def _decode_response(response):
    _check_response_code(response)
    return json.loads(response.content.decode())


def _build_authorization_header(token):
    return {"Authorization": "Bearer {}".format(token)}


class Cheddar:
    def __init__(self, host, port=443, secure=True):
        self._secure = secure
        self._port = port
        self._host = host
        self._executor = ThreadPoolExecutor(max_workers=1)

    def stop(self):
        self._executor.shutdown()

    @property
    def _hostname(self):
        fragments = ["https" if self._secure else "http", "://", self._host]
        if self._port is not None:
            fragments.append(":")
            fragments.append(str(self._port))

        return "".join(fragments)

    def authenticate(self, email, password):
        def request_authentication():
            response = post(self._hostname + "/api/authentications", auth=(email, password), verify=False)
            user_details = _decode_response(response)
            user_details["email"] = email

            return user_details

        return Promise(self._executor.submit(request_authentication))

    def get_identities(self, phrase, token):
        def request_identities():
            response = get("{0}/api/identities?q={1}".format(self._hostname, phrase), verify=False,
                           headers=(_build_authorization_header(token)))

            return {
                "total_count": response.headers.get("X-Total-Count"),
                "identities": _decode_response(response)
            }

        return Promise(self._executor.submit(request_identities))

    def assign_identifier(self, name, type_, works, token):
        def assign_identifier():
            data = {
                "type": type_,
                "name": name,
                "works": [{"title": work} for work in works]
            }

            response = post("{0}/api/identities".format(self._hostname), data=json.dumps(data), verify=False,
                            headers=(_build_authorization_header(token)))

            return _decode_response(response)

        return Promise(self._executor.submit(assign_identifier))
