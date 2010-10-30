from google.appengine.ext.db import djangoforms
from models import *

class RecipeForm(djangoforms.ModelForm):
    class Meta:
        model = Recipe
        exclude = [
            'added_by',
            'picture',
        ]

class IngredientForm(djangoforms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = [
            'recipe',
        ]
