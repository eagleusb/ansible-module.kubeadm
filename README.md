# ansible-module-kubeadm

Ansible module and module utils to initialize Kubernetes cluster with the help of kubeadm.

## kubeadm

### GoDoc
-  [kubeadm](https://godoc.org/k8s.io/kubernetes/cmd/kubeadm)
-  [kubeadm/v1beta1](https://godoc.org/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta1)
-  [kubeadm/v1beta2](https://godoc.org/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta2)

## Ansible

### Plugin

Valid plugin path:
-  `~/.ansible/plugins/$plugin_type`
-  `/usr/share/ansible/plugins/$plugin_type`

Plugin(s) directories for auto-loading:
-  `action_plugins*`
-  `cache_plugins`
-  `callback_plugins`
-  `connection_plugins`
-  `filter_plugins*`
-  `inventory_plugins`
-  `lookup_plugins`
-  `shell_plugins`
-  `strategy_plugins`
-  `test_plugins*`
-  `vars_plugins`

### Module

Valid module path:
- `ANSIBLE_LIBRARY` environment variable with `:` separated path list
- `~/.ansible/plugins/modules/`
- `/usr/share/ansible/plugins/modules/`
- `library/` directory alongside a playbook or inside a role

### Test

```shell
$ ANSIBLE_LIBRARY=. ANSIBLE_MODULE_UTILS=kubeadm/module_utils \
  ansible-playbook test/play.yml [--ask-become-pass]
```
