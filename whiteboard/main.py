import webapp2

class HomeHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write('Hello, world!')

routes = [
    ('/', HomeHandler),
]

app = webapp2.WSGIApplication(routes, debug=True)
