from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from google.appengine.api import users
from google.appengine.ext.webapp import template

from handlers.base import BaseHandler
from models.ghosts import Ghost
from models.users import User
from utils.path_setter import set_path


class Overview(BaseHandler):
    TEMPLATE_NAME = 'overview.html'

    def get(self):
        ghost_instances = Ghost.query().order(Ghost.name).fetch()
        log_url_linktext = ''
        log_url = ''
        pick_linktext = ''
        current_user = None

        google_user = users.get_current_user()
        if google_user:
            current_user = self.session.get('current_user', None)
            log_url = users.create_logout_url(self.request.uri)
            log_url_linktext = 'Logout'
            pick_linktext = 'Change your current Phantom name'
            if not current_user:
                user = User.query(User.google_user_id==google_user.user_id()).get()
                if user:
                    associated_ghost = Ghost.query(Ghost.user==user.key).get()
                    current_user = {'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'email': user.email,
                                    'ghost': associated_ghost.name}
                    self.session['current_user'] = current_user
                pick_linktext = 'Get a Phantom name'
        else:
            # delete user session if exists (after logout)
            if 'current_user' in self.session:
                del self.session['current_user']
            log_url = users.create_login_url(self.request.uri)
            log_url_linktext = 'Login'
            pick_linktext = 'Get a Phantom name'

        ghosts = []
        for ghost_instance in ghost_instances:
            user_email = ''
            full_name = ''
            if ghost_instance.taken:
                ghost_user = ghost_instance.user.get()
                user_email = ghost_user.email
                full_name = ' '.join((ghost_user.first_name, ghost_user.last_name))

            ghosts.append({'name': ghost_instance.name,
                           'taken': ghost_instance.taken,
                           'user_email': user_email,
                           'user_full_name': full_name})

        template_values = {
            'ghosts': ghosts,
            'current_user': current_user,
            'log_url': log_url,
            'log_url_linktext': log_url_linktext,
            'pick_linktext': pick_linktext
        }

        path = set_path(self.TEMPLATE_NAME)
        self.response.out.write(template.render(path, template_values))
