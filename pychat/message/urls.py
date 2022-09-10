from django.urls import path
from . import views 

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name="home"),
    path('<pk>/', views.dm_detail, name="dm")
]

urlpatterns += staticfiles_urlpatterns()