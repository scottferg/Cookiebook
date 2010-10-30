# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from django.contrib import admin

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',

    (r'^$', 'recipes.views.recipe_list'),
    (r'^recipe/add/$', 'recipes.views.add_recipe'),
    (r'^recipe/(?P<recipe_id>[^/]+)/$', 'recipes.views.recipe_detail'),
    (r'^recipe/(?P<recipe_id>[^/]+)/edit/$', 'recipes.views.edit_recipe'),

) + urlpatterns
