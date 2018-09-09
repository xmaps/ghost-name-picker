from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from google.appengine.ext import ndb


class User(ndb.Model):
    """
    Class that represents the users of the system.
    Only saves after they generated ghost name.
    If they login with user account no record is saved.
    """
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    google_user_id = ndb.StringProperty(required=True)
