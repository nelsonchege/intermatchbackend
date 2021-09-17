from django.urls import path
from  .views import Hello , RegisterView , LoginView , UserView , LogoutView , CreateProfileView,UserProfiles

# this are the urls that are used to access account
urlpatterns = [
    path('hello/',Hello.as_view()),
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('userauth/',UserView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('CreateProfile/',CreateProfileView.as_view()),
    path('profile/',UserProfiles.as_view()),
]