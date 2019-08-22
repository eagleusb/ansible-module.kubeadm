KUBEADM_MOD_CONFIG = {
  "support_check_mode": True,
  # "required_together": [['init', 'name']],
}

KUBEADM_ARG_SPEC = {
  "version": {
    "type": "bool",
    "default": False,
  },
  "init": {
    "type": "bool",
    "default": False,
  },
  "force": {
    "type": "bool",
    "default": False,
  },
  "name": {
    "type": "str",
    "required": False,
  },
}
