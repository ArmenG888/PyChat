from django.urls import path
from . import views 

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('register/', views.register, name="register"),

]

urlpatterns += staticfiles_urlpatterns()