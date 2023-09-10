from venv import logger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from . import views
from .models import Movie, UsersWatchedMovies
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def movie_recommendation_view(request):
    if request.method == "POST" and request.user.is_authenticated:
        movie_id = request.POST.get('movie_id')
        if movie_id:
            movie = Movie.objects.get(pk=movie_id)
            UsersWatchedMovies.objects.create(user=request.user, movie=movie)
            # movie.watched = True
            # movie.save()
        
        return HttpResponseRedirect(request.path_info)

    elif request.method == "GET" and request.user.is_authenticated:
      # The context/data to be presented in the HTML template
      context = generate_movies_context_for_user(request.user)
      # Render a HTML page with specified template and context
      return render(request, 'movierecommender/movie_list.html', context)
    else:
      context = generate_content_for_unauth_users()
      return render(request, 'movierecommender/movie_list.html', context)



def generate_movies_context_for_user(user):

    context = {}
    watched_movie_ids = UsersWatchedMovies.objects.filter(user=user).values_list('movie_id', flat=True)
    watched_genres = UsersWatchedMovies.objects.filter(user=user).values_list('movie__genres', flat=True)
    # recommended_movies = Movie.objects.exclude(id__in=watched_movie_ids).order_by('-vote_count')[:30]
    
    recommended_movies = Movie.objects.filter(genres__in=watched_genres).exclude(id__in=watched_movie_ids).order_by('-vote_count')[:30]
    
    if not recommended_movies:
        recommended_movies = Movie.objects.exclude(id__in=watched_movie_ids).order_by('vote_count')[:30]
    

    context['movie_list'] = recommended_movies

    return context

def generate_content_for_unauth_users():
    
    context = {}

    top_rated_movies = Movie.objects.all().order_by('-vote_count')[:30]

    context['movie_list'] = top_rated_movies
    return context


def login_request(request):
    context = {}
    #Handles post request
    if request.method == "POST":
        #Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
    
        #Try to check if provided credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            #If user is valid, call login method and login current user
            login(request, user)
            return redirect('movie_recommender:recommendations')
        else:
            return render(request, 'movierecommender/user_login.html', context)
    else:
        return render(request, 'movierecommender/user_login.html', context)


def registration_request(request):
    context = {}

    if request.method == "GET":
        return render(request, 'movierecommender/user_registration.html', context)

    elif request.method == "POST":
        # Get user information from request.POST
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        password = request.POST['psw']
        
        user_exists = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exists = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user", format(username))

        if not user_exists:
            #Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)

            login(request, user)
            return redirect('movie_recommender:recommendations')
        else:
            return render(request, 'movierecommender/user_registration.html', context)


def logout_request(request):
    #Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))

    #Logout user in the request
    logout(request)
    #Redirect user back to course list view
    return redirect('movie_recommender:recommendations')

