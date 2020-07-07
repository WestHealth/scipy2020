"""Tornado handlers for logging out of the notebook.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from ..base.handlers import IPythonHandler
import os

class LogoutHandler(IPythonHandler):

    def get(self):
        self.clear_login_cookie()
        if self.login_available:
            message = {'info': 'Successfully logged out.'}
        else:
            message = {'warning': 'Cannot log out.  Notebook authentication '
                       'is disabled.'}

        self.redirect(os.environ['logout_url'])

default_handlers = [(r"/logout", LogoutHandler)]
