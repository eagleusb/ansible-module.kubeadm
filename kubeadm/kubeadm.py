#!/usr/bin/env python3

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
from template import KubeadmTemplate


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

  def __kubeadm_version(self):
    _, stdout, _ = self.module.run_command(['kubeadm', 'version'], check_rc=True)
    self.result['kubeadm_version'] = stdout
    self.result['changed'] = True

  def __kubeadm_init_template(self):
    template = KubeadmTemplate('init')
    self.kubeadm_init_config = template.written

  def __kubeadm_init_run(self):
    _, stdout, _ = self.module.run_command(
      ['kubeadm', 'init', '--dry-run', '--config', self.kubeadm_init_config], check_rc=True
    )
    self.result['kubeadm_init'] = stdout
    self.result['changed'] = True

  def __destructure(self, dict_to_destructure, *args):
    return [dict_to_destructure[key] for key in args]

  def run(self):
    # print(self.module.params)
    # print(self.module.tmpdir)

    # destructure all the input parameters
    version, init, config = self.__destructure(self.module.params, 'version', 'init', 'config')
    # print(config)

    if self.module.check_mode:
      self.module.exit_json(**self.result)

    if version:
      self.__kubeadm_version()

    if init or init == 'yes':
      self.__kubeadm_init_template()
      self.__kubeadm_init_run()

    self.module.exit_json(**self.result)


def main():
  KubeadmModule().run()

if __name__ == '__main__':
  main()
