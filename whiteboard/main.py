import os

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class HomeHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('home.html')
    self.response.write(template.render())

routes = [
    ('/', HomeHandler),
]

app = webapp2.WSGIApplication(routes, debug=True)
