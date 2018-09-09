from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os


def set_path(file_name):
    return os.path.join(*[os.path.dirname(__file__), '..', 'templates', file_name])
