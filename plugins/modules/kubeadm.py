#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {"metadata_version": "0.1.0", "status": ["preview"], "supported_by": "community"}

DOCUMENTATION = """
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
"""

EXAMPLES = """
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
"""

RETURN = """
original_message:
  description: The original name param that was passed in
  type: str
  returned: always
message:
  description: The output message that the test module generates
  type: str
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.kubeadm_config import KUBEADM_MOD_CONFIG, KUBEADM_ARG_SPEC
from ansible.module_utils.kubeadm_template import KubeadmTemplate


class KubeadmModule(object):
    def __init__(self):
        self.result = {"changed": False, "rc": 0, "msg": "", "stdout": "", "stderr": ""}
        self.module = AnsibleModule(
            argument_spec=KUBEADM_ARG_SPEC,
            supports_check_mode=KUBEADM_MOD_CONFIG.get("supports_check_mode", False),
            required_together=KUBEADM_MOD_CONFIG.get("required_together", []),
        )

    def _destructure(self, dict_to_destructure, *args):
        return [dict_to_destructure[key] for key in args]

    def _kubeadm_init_template(self):
        template = KubeadmTemplate("init")
        self.kubeadm_init_config = template.written

    def _kubeadm_init_cmd(self, parameter_list):
        pass

    def _kubeadm_init_run(self):
        cmd = [
            "kubeadm",
            "--skip-headers",
            "--v=2",
            "init",
            "--dry-run",
            "--ignore-preflight-errors=none",
            "--config",
            self.kubeadm_init_config,
        ]
        rc, stdout, stderr = self.module.run_command(cmd, check_rc=False)
        if rc == 0:
            self.result["msg"] = "kubeadm init succeed"
            self.result["stdout"] = stdout
            self.result["changed"] = True
        else:
            self.result["rc"] = rc
            self.result["msg"] = "kubeadm init failed"
            self.result["stderr"] = stderr
            self.module.fail_json(cmd=self.module._clean_args(cmd), **self.result)

    def run(self):
        # destructure all the input parameters
        init, config = self._destructure(self.module.params, "init", "config")

        if self.module.check_mode:
            self.module.exit_json(**self.result)

        if init or init == "yes":
            self._kubeadm_init_template()
            self._kubeadm_init_run()

        self.module.exit_json(**self.result)


def main():
    KubeadmModule().run()


if __name__ == "__main__":
    main()
