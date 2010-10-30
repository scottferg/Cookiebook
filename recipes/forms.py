from django import forms
from models import *

class RecipeForm(forms.Form):
    title       = forms.CharField()
    description = forms.CharField(widget = forms.widgets.Textarea())
    directions  = forms.CharField(widget = forms.widgets.Textarea())
    serves     = forms.CharField(help_text = 'eg: 4 people')

class IngredientForm(forms.Form):
    description = forms.CharField()
