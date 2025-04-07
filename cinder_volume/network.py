# Copyright 2025 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import socket

import pyroute2

LOG = logging.getLogger(__name__)


def _get_local_ip_by_default_route() -> str:
    """Get host IP from default route interface."""
    with pyroute2.NDB() as ndb:
        default_route_ifindex = ndb.routes["default"]["oif"]
        iface = ndb.interfaces[default_route_ifindex]
        try:
            ipaddr = iface.ipaddr[socket.AF_INET]
        except KeyError:
            ipaddr = iface.ipaddr[socket.AF_INET6]
        return ipaddr["address"]


def get_default_ip() -> str:
    try:
        return _get_local_ip_by_default_route()
    except Exception:
        LOG.warning(
            "Failed to get local IP by default route, falling back to localhost",
            exc_info=True,
        )
        return "127.0.0.1"
