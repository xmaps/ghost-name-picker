from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from google.appengine.ext import ndb

from models.users import User


class Ghost(ndb.Model):
    """
    Class that represents the Ghost names in the system.
    """
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    taken = ndb.BooleanProperty(default=False)
    user = ndb.KeyProperty(User)

