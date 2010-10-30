from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app, login_required

from django.utils import simplejson

from recipes.models import *

class RecipeListRPC(webapp.RequestHandler):
    @login_required
    def get(self):
        recipe_list = Recipe.all().order('-published').fetch(50)

        self.response.out.write(simplejson.dumps([recipe.export_to_dict() for recipe in recipe_list]))

application = webapp.WSGIApplication([
                                      (r'/api/recipes/$', RecipeListRPC),
                                     ], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
