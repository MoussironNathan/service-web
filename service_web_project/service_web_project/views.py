import json
from django.shortcuts import render
import requests
from .utils import get_db_handle


def getImg(idMovie):
    try:
        url = "https://api.themoviedb.org/3/movie/%i/images" % idMovie
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMmZiY2NjNzA0MmM4NjQ2ODNlZWFjYzIwNGI3NmFmZiIsInN1YiI6IjY0N2Q5MWU3Y2Y0YjhiMDBhODc4N2YxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mzdeeD2vVHgRNLkgO4z9h8GxzUMcPKLbE28bhuWihJg"
        }
        response = json.loads(requests.get(url, headers=headers).text)
        imgLink = None
        if response["posters"]:
            imgLink = response["posters"][0]["file_path"]
        return imgLink
    except:
        return None


def getTitle(idMovie):
    try:
        url = "https://api.themoviedb.org/3/movie/%i?language=en-EN" % idMovie
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMmZiY2NjNzA0MmM4NjQ2ODNlZWFjYzIwNGI3NmFmZiIsInN1YiI6IjY0N2Q5MWU3Y2Y0YjhiMDBhODc4N2YxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mzdeeD2vVHgRNLkgO4z9h8GxzUMcPKLbE28bhuWihJg"
        }
        response = json.loads(requests.get(url, headers=headers).text)
        title = response["title"]

        return title
    except:
        return "Title not available"


def getLikes(id):
    client = get_db_handle()
    db = client['sw']
    collection_name = db['moviesLikes']
    likes = collection_name.find_one({"movie_id": id}, {"likes": 1})
    if likes:
        return likes.get("likes")
    else:
        return 0


def addLike(request, id):
    client = get_db_handle()
    db = client['sw']
    collection_name = db['moviesLikes']
    if collection_name.find_one({"movie_id": id}):
        collection_name.update_one({'movie_id': id}, {'$inc': {'likes': 1}})
    else:
        collection_name.insert_one({'movie_id': id, "likes": 1})
    return movie_details(request, id)


def disLike(request, id):
    client = get_db_handle()
    db = client['sw']
    collection_name = db['moviesLikes']
    if collection_name.find_one({"movie_id": id}):
        collection_name.update_one({'movie_id': id}, {'$inc': {'likes': -1}})
    return movie_details(request, id)


def home(request, page=1):
    url = "https://api.themoviedb.org/3/movie/changes?page=%i" % page
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMmZiY2NjNzA0MmM4NjQ2ODNlZWFjYzIwNGI3NmFmZiIsInN1YiI6IjY0N2Q5MWU3Y2Y0YjhiMDBhODc4N2YxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mzdeeD2vVHgRNLkgO4z9h8GxzUMcPKLbE28bhuWihJg"
    }
    response = json.loads(requests.get(url, headers=headers).text)
    listMovie = []
    for movie in response["results"]:
        listMovie.append({"id": movie["id"], "title": getTitle(movie["id"]), "image": getImg(movie["id"]),
                          "likes": getLikes(movie["id"])})
    return render(request, "movies.html", {
        "listMovie": listMovie
    })


def movie_details(request, id):
    try:
        url = "https://api.themoviedb.org/3/movie/%i?language=en-US" % id
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMmZiY2NjNzA0MmM4NjQ2ODNlZWFjYzIwNGI3NmFmZiIsInN1YiI6IjY0N2Q5MWU3Y2Y0YjhiMDBhODc4N2YxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mzdeeD2vVHgRNLkgO4z9h8GxzUMcPKLbE28bhuWihJg"
        }
        response = json.loads(requests.get(url, headers=headers).text)
        critere = ['id', 'adult', 'genres', 'overview', 'poster_path', 'release_date', 'runtime', 'spoken_languages',
                   'title']
        donnees = {}
        for index, value in response.items():
            if index in critere:
                donnees.update({index: value})
        likes = getLikes(id)
        donnees.update({'likes': likes})
        return render(request, "movie_details.html", {
            "donnees": donnees
        })
    except:
        return render(request, "not_founded.html")
