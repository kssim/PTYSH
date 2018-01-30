# -*- coding: utf-8 -*-

"""
Modules related to structure used throughout PTYSH.
"""

from collections import OrderedDict

from yaml import Loader
from yaml import MappingNode


class _Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton("Singleton", (object,), {})): pass


class Status(Singleton):

    """
    Class for checking status in PTYSH
    You can check the login(enable) status, the depth of the node, and the name of the node.
    """

    ROOT_DEPTH = 0
    CONFIGURE_DEPTH = 1

    def __init__(self):
        self._login = False
        self._module_depth = self.ROOT_DEPTH
        self._current_node = []

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, state):
        self._login = state

    @property
    def module_depth(self):
        return self._module_depth

    def increase_module_depth(self):
        self._module_depth += 1

    def decrease_module_depth(self):
        self._module_depth -= 1

    @property
    def current_node(self):
        return "" if len(self._current_node) == 0 else self._current_node[-1]

    def push_current_node(self, node_name):
        self._current_node.append(node_name)

    def pop_current_node(self):
        self._current_node.pop()


class OrderedDictYAMLLoader(Loader):

    """
    When loading a YAML file, use OrderDedDictionary to maintain the order of the loaded settings.
    PyYaml does not support OrderedDictionary, so I created a Loader to make OrderdedDictionary available.
    This source code was referenced in the gist below.
      - https://gist.github.com/enaeseth/844388
    """

    def __init__(self, *args, **kwargs):
        Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u"tag:yaml.org,2002:map", type(self).construct_yaml_map)
        self.add_constructor(u"tag:yaml.org,2002:omap", type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data

        value = self.construct_mapping(node)
        if value is not None:
            data.update(value)

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            return None

        self.flatten_mapping(node)
        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except:
                return None

            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping
