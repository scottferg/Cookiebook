from google.appengine.ext import db
from google.appengine.ext import search

class Recipe(search.SearchableModel):
    title       = db.StringProperty()
    description = db.TextProperty()
    published   = db.DateTimeProperty(auto_now_add = True)
    picture     = db.BlobProperty()
    directions  = db.TextProperty()
    serves      = db.StringProperty()
    added_by    = db.UserProperty()

    def export_to_dict(self):
        return {
            'key'         : '%s' % self.key(),
            'title'       : self.title,
            'description' : self.description,
            'published'   : self.published.strftime('%B %d, %Y'),
            'directions'  : self.directions,
            'added_by'    : self.added_by.nickname(),
            'ingredients' : [ingredient.description for ingredient in self.ingredient_set],
        }

class Ingredient(db.Model):
    recipe      = db.ReferenceProperty(Recipe)
    description = db.StringProperty()
