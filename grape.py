#!/usr/bin/python
# -*- coding: utf-8 -*-

# Ron Widler <ron@einfach.org>
# Inspired by the hipchat and mattermost modules

# This module is free software: you can redistribute it and/or modify
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
short_description: Send a message to Grape
description:
    - Send a message to a Grape room using a custom webhook
options:
  webhook_url:
    description:
      - Url of the webhook to send to
    required: true
  username:
    description:
      - Username to show up in the message
    default: Ansible
  msg:
    description:
      - Message to send
    required: true
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used
        on personally controlled sites using self-signed certificates.
    default: yes
    choices:
      - 'yes'
      - 'no'


requirements: [ ]
author: "WIDLER Ron (@r900)"
'''

EXAMPLES = '''
- grape:
    webhook_url: "https://chatgrape.com/services/hook/custom/1/c94de931ec494e695d3e347c68c9e2f3/
    username: "My bot"
    msg: "Task A finished"

- grape:
    webhook_url: "https://grape-test.example.com"
    msg: "Sending to instance with self-signed SSL certs"
    validate_certs: no

'''

# ===========================================
# Grape module specific support methods.
#

from ansible.module_utils.pycompat24 import get_exception
from ansible.module_utils.urls import fetch_url

# import module snippets
from ansible.module_utils.basic import AnsibleModule


def send_msg(module, webhook_url, username, msg):
    '''Send message to webhook'''

    params = {}
    params['username'] = username
    params['text'] = msg

    url = webhook_url
    data = module.jsonify(params)

    headers = {'Content-type': 'application/json'}

    if module.check_mode:
        # In check mode, exit before actually sending the message
        module.exit_json(changed=False,
                         webhook_url=webhook_url,
                         username=username,
                         msg=msg)

    response, info = fetch_url(module,
                               url=url,
                               data=data,
                               headers=headers,
                               method="POST")

    if info['status'] == 200:
        return response.read()
    else:
        module.fail_json(msg="Failed to send message, return status={}".format(info['status']))


# ===========================================
# Module execution.
#

def main():

    module = AnsibleModule(
        argument_spec=dict(
            webhook_url=dict(required=True, type='str'),
            username=dict(default='Ansible', type='str'),
            msg=dict(required=True, type='str'),
            validate_certs=dict(default='yes', type='bool'),
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
        module.fail_json(msg="Unable to send message: %s" % e)

    changed = True
    module.exit_json(changed=changed, username=username, msg=msg)


if __name__ == '__main__':
    main()
