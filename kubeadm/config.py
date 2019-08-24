KUBEADM_TEMPLATE_VARS = {
  "init": {
    "apiVersion": "kubeadm.k8s.io/v1beta2",
    "apiAddress": "0.0.0.0",
    "apiPort": "6443",
    "kVersion": "stable-1",
    # "clusterName": "foobar",
    "imageRepo": "k8s.gcr.io",
    # "controlPlaneEndpoint": "",
    "tlsVersion": "VersionTLS12",
    "dns": {
      "type": "CoreDNS",
      "domain": "cluster.local",
    },
    "network": {
      "podSubnet": "10.244.0.0/16",
      "serviceSubnet": "10.96.0.0/12",
    },
    "cert": {
      "sans": [],
    },
    "rate": {
      "maxBytes": "131072",
      "maxMutatingReqs": "200",
      "maxReqs": "400",
    },
    "etcd": {
      "endpoints": [],
      "ca": "/etc/kubernetes/pki/etcd/ca.crt",
      "cert": "/etc/kubernetes/pki/etcd/client.crt",
      "key": "/etc/kubernetes/pki/etcd/client.key",
    }
  },
}

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
    "choices": ['yes', 'no', True, False],
    "aliases": ['create', 'initialize'],
  },
  "config": {
    "type": "dict",
    "default": KUBEADM_TEMPLATE_VARS,
    "aliases": ['cfg', 'configuration'],
  },
}
