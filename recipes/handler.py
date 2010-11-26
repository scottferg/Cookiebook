from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import wraps
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

from recipes.models import *

def json_response(view):
    def wrapper(request, *args, **kwargs):
        data = view(request, *args, **kwargs)

        response = HttpResponse(simplejson.dumps(data, cls = DjangoJSONEncoder))
        return response
    return wraps(view)(wrapper)

@login_required
@json_response
def recipe_list(self):
    recipe_list = Recipe.all().order('-published').fetch(10)

    return [recipe.export_to_dict() for recipe in recipe_list]
