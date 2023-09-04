from django.urls import path
from . import views

app_name = 'movie_recommender'

urlpatterns = [
    # route is a string contains a URL pattern
    path(route='', view=views.movie_recommendation_view, name='recommendations'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path('registration/', views.registration_request, name='registration'),

]