import cgi, os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app, login_required

from recipes.forms import *

class Image(webapp.RequestHandler):
    def get(self):
        recipe = db.get(self.request.get('img_id'))

        if recipe.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(recipe.picture)
        else:
            self.error(404)

class Recipes(webapp.RequestHandler):
    @login_required
    def get(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

        recipe_list = Recipe.all().order('-published').fetch(50)

        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {
            'recipe_list': [recipe.export_to_dict() for recipe in recipe_list],
        }))

class RecipeCategory(webapp.RequestHandler):
    @login_required
    def get(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

        path = os.path.join(os.path.dirname(__file__), 'templates/base.html')
        self.response.out.write(template.render(path, {}))

class RecipeDetail(webapp.RequestHandler):
    @login_required
    def get(self, recipe_id):
        recipe = db.get(recipe_id)

        if not recipe:
            self.redirect('/')

        path = os.path.join(os.path.dirname(__file__), 'templates/detail.html')
        self.response.out.write(template.render(path, {
            'recipe'           : recipe,
            'show_edit_button' : users.get_current_user() == recipe.added_by and True or False
        }))

class AddRecipe(webapp.RequestHandler):
    @login_required
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/add_recipe.html')
        self.response.out.write(template.render(path, {
            'title': 'Add a recipe',
            'form': RecipeForm(),
        }))

    def post(self):
        recipe = Recipe(
            title       = cgi.escape(self.request.get('title')),
            description = cgi.escape(self.request.get('description')),
            directions  = cgi.escape(self.request.get('directions')),
            serves      = cgi.escape(self.request.get('serves')),
            added_by    = users.get_current_user()
        )

        picture = self.request.get('picture')

        if picture:
            recipe.picture = picture

        recipe.put()

        ingredients = self.request.get('ingredient', allow_multiple = True)

        for ingredient in ingredients:
            if ingredient:
                new_ingredient = Ingredient(
                    recipe      = recipe,
                    description = ingredient
                )
                new_ingredient.put()

        self.redirect('/recipe/%s/' % recipe.key())

class EditRecipe(webapp.RequestHandler):
    @login_required
    def get(self, recipe_id):
        recipe = db.get(recipe_id)

        if not recipe:
            self.redirect('/')

        path = os.path.join(os.path.dirname(__file__), 'templates/edit_recipe.html')
        self.response.out.write(template.render(path, {
            'recipe'           : recipe,
        }))

    def post(self, recipe_id):
        recipe = db.get(recipe_id)

        recipe.title       = cgi.escape(self.request.get('title'))
        recipe.description = cgi.escape(self.request.get('description'))
        recipe.directions  = cgi.escape(self.request.get('directions'))
        recipe.serves      = cgi.escape(self.request.get('serves'))
        recipe.put()

        # Delete any ingredients we already have and rewrite them
        for ingredient in db.GqlQuery('SELECT * FROM Ingredient WHERE recipe = :1', recipe):
            ingredient.delete()

        # Write out new ingredients
        for ingredient in self.request.get('ingredient', allow_multiple = True):
            if ingredient:
                new_ingredient = Ingredient(
                    recipe      = recipe,
                    description = ingredient
                )
                new_ingredient.put()

        self.redirect('/recipe/%s/' % recipe.key())

application = webapp.WSGIApplication([
                                      ('/', Recipes),
                                      (r'/recipes/(.*)/', RecipeCategory),
                                      ('/recipe/add/', AddRecipe),
                                      (r'/recipe/(.*)/', RecipeDetail),
                                      (r'/edit/(.*)/', EditRecipe),
                                      ('/image', Image),
                                     ], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
