#!/usr/bin/python

ANSIBLE_METADATA = {
  'metadata_version': '0.1.0',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ansible-module-kubeadm
short_description: Kubernetes kubeadm module
version_added: "2.8"
description:
    - "Bootstrap and manage Kubernetes cluster with kubeadm"
options:
  name:
    description:
      - This is the message to send to the test module
    required: true
  new:
    description:
      - Control to demo if the result of this module is changed or not
    required: false
extends_documentation_fragment: []
author:
  - Leslie-Alexandre DENIS (@eagleusb)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_test:
    name: fail me
'''

RETURN = '''
original_message:
  description: The original name param that was passed in
  type: str
  returned: always
message:
  description: The output message that the test module generates
  type: str
  returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from config import KUBEADM_MOD_CONFIG, KUBEADM_ARG_SPEC


class KubeadmModule(object):

  def __init__(self, *args, **kwargs):
    # super().__init__(*args, **kwargs)
    self.result = {
      "changed": False,
    }
    self.module = AnsibleModule(
      argument_spec = KUBEADM_ARG_SPEC,
      supports_check_mode = KUBEADM_MOD_CONFIG.get('supports_check_mode', False),
      required_together = KUBEADM_MOD_CONFIG.get('required_together', []),
    )

  def __version(self):
    rc, stdout, stderr = self.module.run_command(['kubeadm', 'version'], check_rc=True)
    self.result['kubeadm_version'] = stdout
    self.result['changed'] = True

  def run(self):
    print(self.module.params)
    print(self.module.tmpdir)

    if self.module.check_mode:
      self.module.exit_json(**self.result)

    if self.module.params['version']:
      self.__version()

    self.module.exit_json(**self.result)


def main():
  KubeadmModule().run()

if __name__ == '__main__':
  main()
