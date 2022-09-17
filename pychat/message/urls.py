from django.urls import path
from . import views 

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name="home"),
    path('chat/<pk>/', views.dm_detail, name="dm"),
    path('ajax/<pk>', views.ajax, name="ajax")
]

urlpatterns += staticfiles_urlpatterns()