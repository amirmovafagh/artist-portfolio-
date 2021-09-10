from django.urls import path

from works import views

app_name = 'works'

urlpatterns = [
    path('<str:slug>/', views.WorkDetail, name='WorkDetail'),
    path('category/<str:slug>/', views.CategoryWorkList, name='CategoryWorkList'),
]
