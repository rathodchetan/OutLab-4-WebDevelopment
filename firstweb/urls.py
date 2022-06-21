from django.urls import path
from . import views

app_name = 'firstweb' 

urlpatterns = [
    path("register", views.register, name= 'register'),
    path("Explore", views.explore, name= 'Explore'),
    path("MyProfile", views.myprofile, name= 'MyProfile'),
    path("ALLProfile/<str:usernm>", views.allprofile, name= 'ALLProfile'),
    path("Update", views.update, name= 'Update'),
]
