from django.urls import path
from . import views

app_name = 'cryptoriseapp'
urlpatterns = [
   path('', views.home, name='home page'),
]