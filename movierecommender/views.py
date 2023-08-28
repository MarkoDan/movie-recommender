from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from . import views
from .models import Movie
from django.shortcuts import render

# HINT: Create a view to provide movie recommendations list for the HTML template

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
        

# def get_movie_recommendations(request):
#     start = int(request.GET.get('start', 0))
#     end = int(request.GET.get('end', start + 15))

#     movies = Movie.objects.filter(watched=False).order_by('-vote_count')[start:end]

#     #Convert the movies to a list of dictionaries for JSON serialization
#     movies_list = []
#     for movie in movies:
#         movies_list = [{"id": movie.id, "title": movie.title}]

#     return JsonResponse(movies_list, safe=False)