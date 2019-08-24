from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from config import KUBEADM_TEMPLATE_VARS
import os
import tempfile


class KubeadmTemplate(object):
  __slots__ = ['__jinja', '__loaded', '__rendered', 'written']

  def __init__(self, kind):
    current_directory = str(Path(__file__).parent.resolve())
    self.__jinja = Environment(
      loader = FileSystemLoader(current_directory + '/templates'),
      trim_blocks = True,
      lstrip_blocks = True,
    )
    self.templatize(kind)

  def __load(self, template):
    self.__loaded = self.__jinja.get_template(template + '.yml.j2')

  def __render(self, kind):
    self.__rendered = bytes(self.__loaded.render(KUBEADM_TEMPLATE_VARS[kind]), encoding='utf-8')

  def __write(self, kind):
    fd, tmpfile = tempfile.mkstemp(prefix=f'kubeadm_{kind}_')
    with open(tmpfile, 'wb') as file:
      file.write(self.__rendered)
    os.close(fd)
    self.written = tmpfile

  def templatize(self, template):
    self.__load(template)
    self.__render(template)
    self.__write(template)


if __name__ == '__main__':
  test = KubeadmTemplate('init')
  print(test.__dict__)
