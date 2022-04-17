from django import forms
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'],"https://www.themoviedb.org/movie/"+str(movie_id)

def recommend(movie):
    #print(movie)
    mindex = movies[movies['title'].values == movie].index[0]
    distances = sorted(list(enumerate(similarity[mindex])),reverse=True,key = lambda x: x[1])

    recommended_movies = []
    recommended_movies_posters = []
    link=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        a,b=fetch_poster(movie_id)
        recommended_movies_posters.append(a)
        link.append(b)

    Searched_poster,Searched_poster_link=fetch_poster(movies.iloc[mindex].movie_id)
    return recommended_movies, recommended_movies_posters,link,Searched_poster,Searched_poster_link

movies= pickle.load(open('movies.pkl','rb'))
#movies=pd.DataFrame(movies_dict)
#movies_list=sorted(movies_list)
movie_list= [tuple([x,x]) for x in sorted(movies['title'].values)]

similarity= pickle.load(open('similarity.pkl','rb'))

class UserForm(forms.Form):
    movie_name= forms.CharField(label="Search movie here", widget=forms.Select(choices=movie_list))
