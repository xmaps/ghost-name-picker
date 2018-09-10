from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext.webapp import template

from handlers.base import BaseHandler
from models.ghosts import Ghost
from models.users import User
from utils.path_setter import set_path


class NamePicker(BaseHandler):
    """
    Handler class that represents the page to pick/edit the ghost name.
    """
    TEMPLATE_NAME = 'name_picker.html'
    CHANGE_HEADER_TEXT = 'Change your ghost name.'
    CREATE_HEADER_TEXT = 'Create your ghost name.'

    @staticmethod
    def _get_available_ghosts():
        """
        Get three(3) available (not assigned to a user) ghosts.
        Force randomize.

        :return 3 random Ghost instances
        """
        # Ghost.query(Ghost.taken==False).fetch(3, projection=[Ghost.name])
        # would be better but keeps giving the ghosts in the order they are in the database
        all_ghost_keys = Ghost.query(Ghost.taken==False).fetch(keys_only=True)
        selected_keys = random.sample(all_ghost_keys, 3)
        available_ghosts = []
        for selected_key in selected_keys:
            available_ghosts.append(selected_key.get())

        return available_ghosts

    def get(self):
        """Process get requests and displays the page and required info."""

        header_text = self.CREATE_HEADER_TEXT
        # the page requires the user to be logged in so this is always present
        google_user = users.get_current_user()
        current_user = self.session.get('current_user', None)
        # if there's no internal user present in the session
        if not current_user:
            user = User.query(User.google_user_id==google_user.user_id()).get()
            if user:
                associated_ghost = Ghost.query(Ghost.user==user.key).get()
                # create session user and save it to session
                current_user = {'first_name': user.first_name,
                                'last_name': user.last_name,
                                'email': user.email,
                                'ghost': associated_ghost.name}
                self.session['current_user'] = current_user
                header_text = self.CHANGE_HEADER_TEXT
        else:
            header_text = self.CHANGE_HEADER_TEXT

        available_ghosts = self._get_available_ghosts()
        template_values = {
            'available_ghosts': available_ghosts,
            'current_user': current_user,
            'header_text': header_text
        }

        path = set_path(self.TEMPLATE_NAME)
        self.response.out.write(template.render(path, template_values))

    def post(self):
        """Processes the information sent by the page form."""
        current_user = self.session.get('current_user', None)
        assigned_ghost_name = self.request.get('assigned_ghost')
        assigned_ghost = Ghost.query(Ghost.name==assigned_ghost_name).get()

        # check the selected ghost exists in the case there's
        # tampering with the page
        if assigned_ghost:
            # edit current ghost name
            if current_user:
                # get user by email from user on session
                email = current_user['email']
                user = User.query(User.email==email).get()
                # get old ghost name to remove association
                old_ghost = Ghost.query(Ghost.user==user.key).get()
                old_ghost.taken = False
                old_ghost.user = None
                # associate new ghost name
                assigned_ghost.taken = True
                assigned_ghost.user = user.key
                ndb.put_multi([old_ghost, assigned_ghost])
            else:
                # create new user and associate ghost name
                google_user = users.get_current_user()
                email = google_user.email()
                first_name = self.request.get('first_name')
                last_name = self.request.get('last_name')

                user = User(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            google_user_id=google_user.user_id())

                # allocate key to associate until save
                new_user_id = User.allocate_ids(size=1)[0]
                new_user_key = ndb.Key(User, new_user_id)
                user.key = new_user_key
                # associate new user to ghost name
                assigned_ghost.taken = True
                assigned_ghost.user = new_user_key
                ndb.put_multi([user, assigned_ghost])

            # save internal user to session
            self.session['current_user'] = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'ghost': assigned_ghost.name}

            # redirect to main page
            self.redirect('/ghost_name_picker/')
        else:
            # the selected ghost does not exist, refresh page with error message
            available_ghosts = self._get_available_ghosts()
            header_text = self.CHANGE_HEADER_TEXT if current_user is not None else self.CREATE_HEADER_TEXT
            template_values = {
                'available_ghosts': available_ghosts,
                'current_user': current_user,
                'header_text': header_text,
                'error': 'Selected ghost name does not exist.'
            }
            path = set_path(self.TEMPLATE_NAME)
            self.response.out.write(template.render(path, template_values))
