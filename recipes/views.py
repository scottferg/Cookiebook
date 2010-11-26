import cgi, os

from google.appengine.api import images, users
from google.appengine.ext import db

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from recipes.forms import *
from recipes.models import *

def image(request):
    recipe = db.get(request.GET['img_id'])

    if recipe.picture:
        response = HttpResponse(recipe.picture)
        response['Content-Type'] = 'image/png'

        return response
    else:
        self.error(404)

@login_required
def recipe_list(request):
    recipe_list = Recipe.all()

    if 'query' in request.GET.keys():
        for item in request.GET['query'].split(' '):
            recipe_list = recipe_list.search(item)

    recipe_list = recipe_list.order('-published').fetch(50)

    return render_to_response('index.html',
        {
            'recipe_list': [recipe.export_to_dict() for recipe in recipe_list],
        })

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe = Recipe(
                title       = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                directions  = form.cleaned_data['directions'],
                serves      = form.cleaned_data['serves'],
                added_by    = users.get_current_user()
            )

            if 'picture' in request.FILES.keys():
                picture_contents = request.FILES['picture'].read()
                resized_image = images.resize(picture_contents, width=300)

                recipe.picture = db.Blob(resized_image)

            recipe.put()

            for ingredient in request.POST.getlist('ingredient'):
                if ingredient:
                    new_ingredient = Ingredient(
                        recipe      = recipe,
                        description = ingredient
                    )
                    new_ingredient.put()

            return HttpResponseRedirect('/recipe/%s/' % recipe.key())
    else:
        form = RecipeForm()

    return render_to_response('add_recipe.html',
        {
            'title': 'Add a recipe',
            'form': form,
        })

@login_required
def recipe_detail(request, recipe_id):
    recipe = db.get(recipe_id)

    if not recipe:
        return HttpResponseRedirect('/')

    return render_to_response('detail.html',
    {
        'recipe'           : recipe,
        'show_edit_button' : users.get_current_user() == recipe.added_by and True or False
    })

@login_required
def edit_recipe(request, recipe_id):
    recipe = db.get(recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe.title       = form.cleaned_data['title']
            recipe.description = form.cleaned_data['description']
            recipe.directions  = form.cleaned_data['directions']
            recipe.serves      = form.cleaned_data['serves']

            if 'picture' in request.FILES.keys():
                picture_contents = request.FILES['picture'].read()
                resized_image = images.resize(picture_contents, width=300)

                recipe.picture = db.Blob(resized_image)

            recipe.put()

            # Delete any ingredients we already have and rewrite them
            for ingredient in Ingredient.all().filter('recipe =', recipe):
                ingredient.delete()

            # Write out new ingredients
            for ingredient in request.POST.getlist('ingredient'):
                if ingredient:
                    new_ingredient = Ingredient(
                        recipe      = recipe,
                        description = ingredient
                    )
                    new_ingredient.put()

            return HttpResponseRedirect('/recipe/%s/' % recipe.key())

    if not recipe:
        HttpResponseRedirect('/')

    return render_to_response('edit_recipe.html',
    {
        'recipe': recipe,
    })

@login_required
def recipe_category(request):
    pass
