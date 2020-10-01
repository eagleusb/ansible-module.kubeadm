KUBEADM_TEMPLATE_SPEC = {
    "init": """{% set etcdEndpoints = etcd.endpoints %}
{% set apiCertSans = cert.sans -%}

---
apiVersion: "{{ apiVersion }}"
kind: "InitConfiguration"
localAPIEndpoint:
  advertiseAddress: "{{ apiAddress }}"
  bindPort: {{ apiPort }}

---
apiVersion: "{{ apiVersion }}"
kind: "ClusterConfiguration"
kubernetesVersion: "{{ kVersion }}"
certificatesDir: "/etc/kubernetes/pki"
clusterName: "{{ clusterName | default('kubernetes') }}"
imageRepository: "{{ imageRepo | default('k8s.gcr.io') }}"
{% if controlPlaneEndpoint is string %}
controlPlaneEndpoint: "{{ controlPlaneEndpoint }}:{{ apiPort }}"
{% endif %}
{% if etcdEndpoints is sequence() and (etcdEndpoints | length()) is odd() %}
etcd:
  external:
    endpoints:
{% for endpoint in etcdEndpoints %}      - "{{ endpoint }}"{% endfor %}
{% endif %}
{% if etcd.cert is defined %}
    caFile: "{{ etcd.ca | default() }}"
    certFile: "{{ etcd.cert | default() }}"
    keyFile: "{{ etcd.key | default() }}"
{% endif %}
apiServer:
{% if apiCertSans is sequence() and (apiCertSans | length()) > 0 %}
  certSANs:
{% for san in apiCertSans %}    - "{{ san }}"
{% endfor %}
{% endif %}
  extraArgs:
    profiling: "false"
    max-connection-bytes-per-sec: "{{ rate.maxBytes }}"
    max-mutating-requests-inflight: "{{ rate.maxMutatingReqs }}"
    max-requests-inflight: "{{ rate.maxReqs }}"
    {#target-ram-mb: "{{ (ansible_memtotal_mb / 2) | int() }}"#}
    tls-min-version: "{{ tlsVersion }}"
{#
{% if k8s_tokens is defined and k8s_tokens is sequence() %}
    token-auth-file: "/etc/kubernetes/tokens"
  extraVolumes:
    - name: "bearer-tokens"
      hostPath: "/opt/aperikube/tokens"
      mountPath: "/etc/kubernetes/tokens"
      readOnly: true
      pathType: File
{% endif %}
#}
controllerManager:
  extraArgs:
    concurrent-deployment-syncs: "5"
    concurrent-endpoint-syncs: "5"
    concurrent-namespace-syncs: "10"
    concurrent-replicaset-syncs: "5"
    concurrent-service-syncs: "1"
    tls-min-version: "{{ tlsVersion }}"
scheduler:
  extraArgs:
    tls-min-version: "{{ tlsVersion }}"
dns:
  type: "{{ dns.type }}"
networking:
  dnsDomain: "{{ dns.domain | default('cluster.local') }}"
  podSubnet: "{{ network.podSubnet | default() }}"
  serviceSubnet: "{{ network.serviceSubnet | default() }}"

---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration

---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration""",
    "join": """---
apiVersion: kubeadm.k8s.io/v1beta2
kind: JoinConfiguration
caCertPath: /etc/kubernetes/pki/ca.crt
discovery:
  bootstrapToken:
    apiServerEndpoint: kube-apiserver:6443
    token: abcdef.0123456789abcdef
    unsafeSkipCAVerification: true
  timeout: 5m0s
  tlsBootstrapToken: abcdef.0123456789abcdef
nodeRegistration:
  criSocket: /var/run/dockershim.sock
  name: eagleusb
  taints: null""",
}


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
        "dns": {"type": "CoreDNS", "domain": "cluster.local"},
        "network": {"podSubnet": "10.244.0.0/16", "serviceSubnet": "10.96.0.0/12"},
        "cert": {"sans": []},
        "rate": {"maxBytes": "131072", "maxMutatingReqs": "200", "maxReqs": "400"},
        "etcd": {
            "endpoints": [],
            # "cert": {
            #   "ca": "/etc/kubernetes/pki/etcd/ca.crt",
            #   "cert": "/etc/kubernetes/pki/etcd/client.crt",
            #   "key": "/etc/kubernetes/pki/etcd/client.key",
            # },
        },
    }
}


KUBEADM_MOD_CONFIG = {
    "support_check_mode": True,
    # "required_together": [['init', 'name']],
}


KUBEADM_ARG_SPEC = {
    "version": {"type": "bool", "default": False},
    "init": {
        "type": "bool",
        "default": False,
        "choices": ["yes", "no", True, False],
        "aliases": ["create", "initialize"],
    },
    "config": {
        "type": "dict",
        "default": KUBEADM_TEMPLATE_VARS,
        "aliases": ["cfg", "configuration"],
    },
}
