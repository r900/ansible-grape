#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: grape
version_added: "0.1"
short_description: Send a message to  Grape
description:
    - Send a message to a Grape room via custom webhook
options:
  webhook_url:
    description:
      - Url of the webhook to send to
    required: true
  username:
    description:
      - Username to show up in the message
    required: true
  msg:
    description:
      - Message to send
    required: true


requirements: [ ]
author: "WIDLER Ron (@r900)"
'''

EXAMPLES = '''
- grape:
    webhook_url: "https://chatgrape.com/services/hook/custom/1/c94de931ec494e695d3e347c68c9e2f3/
    username: "My bot"
    msg: "Task finished"
'''

# ===========================================
# Grape module specific support methods.
#

import urllib
from ansible.module_utils.pycompat24 import get_exception
from ansible.module_utils.urls import fetch_url

try:
    import json
except ImportError:
    import simplejson as json

# import module snippets
from ansible.module_utils.basic import AnsibleModule


def send_msg(module, webhook_url, username, msg):
    '''Send message to webhook'''

    params = {}
    params['username'] = username
    params['text'] = msg

    url = webhook_url
    data = urllib.urlencode(params)

    if module.check_mode:
        # In check mode, exit before actually sending the message
        module.exit_json(changed=False)

    response, info = fetch_url(module, url, data=data)
    if info['status'] == 200:
        return response.read()
    else:
        module.fail_json(msg="failed to send message, return status=%s" %
                         str(info['status']))


# ===========================================
# Module execution.
#

def main():

    module = AnsibleModule(
        argument_spec=dict(
            webhook_url=dict(required=True),
            username=dict(required=True),
            msg=dict(required=True),
        ),
        supports_check_mode=True
    )

    webhook_url = module.params["webhook_url"]
    username = module.params["username"]
    msg = module.params["msg"]

    try:
        send_msg(module, webhook_url, username, msg)
    except Exception:
        e = get_exception()
        module.fail_json(msg="unable to send msg: %s" % e)

    changed = True
    module.exit_json(changed=changed, username=username, msg=msg)


if __name__ == '__main__':
    main()
