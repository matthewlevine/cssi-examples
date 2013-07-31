import os

import jinja2
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), autoescape=True)


class Message(ndb.Model):
  created = ndb.DateTimeProperty(auto_now_add=True)
  content = ndb.TextProperty()
  user = ndb.UserProperty()


class HomeHandler(webapp2.RequestHandler):
  def get(self, message=None):
    user = users.get_current_user()
    if not user:
      return self.redirect(users.create_login_url('/'))
    logout_url = users.create_logout_url('/')

    message_query = Message.query()
    message_query = message_query.order(-Message.created)
    messages = message_query.fetch(100)

    if message and message not in messages:
      messages.insert(0, message)

    template_values = {'user': user, 'logout_url': logout_url, 'messages': messages}
    template = JINJA_ENVIRONMENT.get_template('home.html')
    self.response.write(template.render(template_values))

  def post(self):
    user = users.get_current_user()
    if not user:
      return self.redirect(users.create_login_url('/'))

    content = self.request.get('message')
    message = Message(content=content, user=user)
    message.put()
    self.get(message)

routes = [
    ('/', HomeHandler),
]

app = webapp2.WSGIApplication(routes, debug=True)
