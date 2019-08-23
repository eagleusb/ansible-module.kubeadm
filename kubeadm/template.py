from jinja2 import Environment, FileSystemLoader
from pathlib import Path

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

class KubeadmTemplate(object):
  def __init__(self, *args, **kwargs):
    # super().__init__(*args, **kwargs)
    current_directory = str(Path(__file__).parent.resolve())
    self.env = Environment(
      loader = FileSystemLoader(current_directory + '/templates'),
      trim_blocks = True,
      lstrip_blocks = True,
    )

  def __load(self, template):
    self.loaded = self.env.get_template(template + '.yml.j2')

  def __render(self, kind):
    self.rendered = self.loaded.render(KUBEADM_TEMPLATE_VARS[kind])

  def templatize(self, template):
    self.__load(template)
    self.__render(template)
    print(self.rendered)

if __name__ == '__main__':
  KubeadmTemplate().templatize('init')
