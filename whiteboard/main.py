import os

import jinja2
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), autoescape=True)


class Message(ndb.Model):
  content = ndb.TextProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)
  user = ndb.UserProperty()


class HomeHandler(webapp2.RequestHandler):
  def get(self, new_message=None):
    # Step 1: Get data from the request.
    user = users.get_current_user()
    if not user:
      return self.redirect(users.create_login_url('/'))
    logout_url = users.create_logout_url('/')

    # Step 2: Process the data.
    message_query = Message.query()
    message_query = message_query.order(-Message.created)
    messages = message_query.fetch(100)

    # If we just created a new message, but didn't fetch it from the query,
    # then insert it at the beginning of the list.
    if new_message and new_message not in messages:
      messages.insert(0, new_message)

    # Step 3: Create a response.
    template_values = {'user': user, 'logout_url': logout_url, 'messages': messages}
    template = JINJA_ENVIRONMENT.get_template('home.html')
    self.response.write(template.render(template_values))

  def post(self):
    # Step 1: Get data from the request.
    user = users.get_current_user()
    if not user:
      return self.redirect(users.create_login_url('/'))

    content = self.request.get('message')

    # Step 2: Process that data.
    message = Message(content=content, user=user)
    message.put()

    # Step 3: Create a response.
    self.get(message)


routes = [
    ('/', HomeHandler),
]

app = webapp2.WSGIApplication(routes, debug=True)
