import os

import jinja2
import webapp2

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class HomeHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      return self.redirect(users.create_login_url('/'))
    logout_url = users.create_logout_url('/')

    template_values = {'user': user, 'logout_url': logout_url}
    template = JINJA_ENVIRONMENT.get_template('home.html')
    self.response.write(template.render(template_values))

  def post(self):
    user = users.get_current_user()
    if not user:
      return self.redirect(users.create_login_url('/'))

    message = self.request.get('message')
    self.response.write(message)

routes = [
    ('/', HomeHandler),
]

app = webapp2.WSGIApplication(routes, debug=True)
