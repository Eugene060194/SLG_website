from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('auth', authorization, name='authorization'),
    path('logout', logout_user, name='logout'),
    path('reg', registration, name='registration'),
    path('textexamples', examples, name='examples'),
    path('mytexts', my_texts, name='mytexts'),
    path('generator', generator, name='generator'),
    path('newtext/<str:number>', generator_new_text),
]
