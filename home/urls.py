from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.ContactMe, name='ContactMe'),
    path('aboutme/', views.AboutMe, name='AboutMe'),
]
