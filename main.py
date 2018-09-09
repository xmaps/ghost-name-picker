from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from webapp2 import Route, WSGIApplication
from webapp2_extras.routes import PathPrefixRoute

from handlers.overview import Overview
from handlers.name_picker import NamePicker
from utils.ghots_setup import ghost_initial_set_up

session_config = {
    'secret_key': 'ghostcatch00p3rsp00dfsdferwerwer43545lzxce',
    'cookie_name': 'ghost-name-picker',
    'session_max_age': 5*86400,
    'cookie_args': {
        'max_age': 5*86400,
    }
}

config = {'webapp2_extras.sessions': session_config}

# [START app]
app = WSGIApplication([
        PathPrefixRoute('/ghost_name_picker', [
            Route('/', Overview, name='home'),
            Route('/pick-name', NamePicker, name='name_picker'),
        ]),
    ],
    config=config,
    debug=True)
# [END app]

# Populates datastore with the default set of ghosts if none exists.
ghost_initial_set_up()


def main():
    app.RUN()


if __name__ == '__main__':
    main()
