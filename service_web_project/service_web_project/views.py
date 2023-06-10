import json
import os
from dotenv import load_dotenv
from django.shortcuts import render
import requests
from .utils import get_db_handle

load_dotenv()


def getImg(idMovie):
    try:
        url = "https://api.themoviedb.org/3/movie/%i/images" % idMovie
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.environ.get('TOKEN')}"
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
            "Authorization": f"Bearer {os.environ.get('TOKEN')}"
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


def searchMovie(recherche, page=1):
    url = "https://api.themoviedb.org/3/search/movie?query=%s&page=%i" % (recherche, page)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.environ.get('TOKEN')}"
    }
    response = json.loads(requests.get(url, headers=headers).text)
    listMovie = []
    for movie in response["results"]:
        listMovie.append({"id": movie["id"], "title": getTitle(movie["id"]), "image": getImg(movie["id"]),
                          "likes": getLikes(movie["id"])})
    return listMovie


def home(request, recherche="", page=1):
    listMovie = []
    if recherche:
        listMovie = searchMovie(recherche, page)
    else:
        url = "https://api.themoviedb.org/3/movie/changes?page=%i" % page
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.environ.get('TOKEN')}"
        }
        response = json.loads(requests.get(url, headers=headers).text)
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
            "Authorization": f"Bearer {os.environ.get('TOKEN')}"
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


def getDetails(idPerson):
    try:
        url = "https://api.themoviedb.org/3/person/%i" % idPerson
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.environ.get('TOKEN')}"
        }
        response = json.loads(requests.get(url, headers=headers).text)
        critere = ['name', 'profile_path']
        donnees = {}
        for index, value in response.items():
            if index in critere:
                donnees.update({index: value})
        return donnees
    except:
        return None


def searchPeople(recherche, page=1):
    url = "https://api.themoviedb.org/3/search/person?query=%s&page=%i" % (recherche, page)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.environ.get('TOKEN')}"
    }
    response = json.loads(requests.get(url, headers=headers).text)
    listPeople = []
    print(response["results"])
    for person in response["results"]:
        listPeople.append({"id": person["id"], "name": getDetails(person["id"])["name"],
                           "profile_path": getDetails(person["id"])["profile_path"]})
    return listPeople


def peoples(request, recherche="", page=1):
    listPeople = []
    if recherche:
        listPeople = searchPeople(recherche, page)
    else:
        url = "https://api.themoviedb.org/3/person/popular?page=%i" % page
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.environ.get('TOKEN')}"
        }
        response = json.loads(requests.get(url, headers=headers).text)
        for person in response["results"]:
            listPeople.append({"id": person["id"], "name": getDetails(person["id"])["name"],
                               "profile_path": getDetails(person["id"])["profile_path"]})
    return render(request, "peoples.html", {
        "listPeople": listPeople
    })


def people_details(request, id):
    try:
        url = "https://api.themoviedb.org/3/person/%i" % id
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.environ.get('TOKEN')}"
        }
        response = json.loads(requests.get(url, headers=headers).text)
        critere = ['id', 'name', 'biography', 'birthday', 'deathday', 'known_for_department', 'place_of_birth',
                   'profile_path']
        donnees = {}
        for index, value in response.items():
            if index in critere:
                donnees.update({index: value})
        return render(request, "people_details.html", {
            "donnees": donnees
        })
    except Exception as error:
        print(error)
        return render(request, "not_founded.html")
