from venv import logger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from . import views
from .models import Movie
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def movie_recommendation_view(request):
    if request.method == "POST":
        movie_id = request.POST.get('movie_id')
        if movie_id:
            movie = Movie.objects.get(pk=movie_id)
            movie.watched = True
            movie.save()
        
        return HttpResponseRedirect(request.path_info)

    elif request.method == "GET":
      # The context/data to be presented in the HTML template
      context = generate_movies_context()
      # Render a HTML page with specified template and context
      return render(request, 'movierecommender/movie_list.html', context)



def generate_movies_context():

    #The context/data to presented in HTML template
    context = {}

    recommended_count = Movie.objects.filter(
        recommended=True
    ).count()

    #If there are no recommended movies
    if recommended_count == 0:
        #Just return the top voted and unwatched movies as popular ones
        movies = Movie.objects.filter(
            watched=False
        ).order_by('-vote_count')[:30]
    
    else:

        #Get the top voted, unwatched, and recommended movies
        movies = Movie.objects.filter(
            watched=False
        ).filter(
            recommended=True
        ).order_by('-vote_count')[:30]
    
    context['movie_list'] = movies

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

# def get_movie_recommendations(request):
#     start = int(request.GET.get('start', 0))
#     end = int(request.GET.get('end', start + 15))

#     movies = Movie.objects.filter(watched=False).order_by('-vote_count')[start:end]

#     #Convert the movies to a list of dictionaries for JSON serialization
#     movies_list = []
#     for movie in movies:
#         movies_list = [{"id": movie.id, "title": movie.title}]

#     return JsonResponse(movies_list, safe=False)