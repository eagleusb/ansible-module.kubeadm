import os
import tempfile

from jinja2 import Environment, DictLoader
from pathlib import Path

from ansible.module_utils.kubeadm_config import KUBEADM_TEMPLATE_SPEC, KUBEADM_TEMPLATE_VARS


class KubeadmTemplate(object):
    __slots__ = ["__jinja", "__loaded", "__rendered", "written"]

    def __init__(self, kind):
        self.__jinja = Environment(
            loader=DictLoader(KUBEADM_TEMPLATE_SPEC), trim_blocks=True, lstrip_blocks=True
        )
        self.templatize(kind)

    def _load(self, template):
        self.__loaded = self.__jinja.get_template(template)

    def _render(self, kind):
        self.__rendered = bytes(self.__loaded.render(KUBEADM_TEMPLATE_VARS[kind]), encoding="utf-8")

    def _write(self, kind):
        fd, tmpfile = tempfile.mkstemp(prefix=f"kubeadm_{kind}_")
        with open(tmpfile, "wb") as file:
            file.write(self.__rendered)
        os.close(fd)
        self.written = tmpfile

    def templatize(self, template):
        self._load(template)
        self._render(template)
        self._write(template)


if __name__ == "__main__":
    test = KubeadmTemplate("init")
    print(test.__dict__)
