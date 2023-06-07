import json

from django.shortcuts import render
import pymongo
import requests

connect_string = 'mongodb+srv://nmoussiron:passworddb@servicewebdb.gyy9vjg.mongodb.net/'

client = pymongo.MongoClient(connect_string)

db = client['sample_medicines']
collection_name = db['medicinedetails']


# let's create two documents
# medicine_1 = {
#     "medicine_id": "RR000123456",
#     "common_name": "Paracetamol",
#     "scientific_name": "",
#     "available": "Y",
#     "category": "fever"
# }
# medicine_2 = {
#     "medicine_id": "RR000342522",
#     "common_name": "Metformin",
#     "scientific_name": "",
#     "available": "Y",
#     "category": "type 2 diabetes"
# }
# # Insert the documents
# collection_name.insert_many([medicine_1, medicine_2])
# # Check the count
# count = collection_name.count_documents({})
# print(count)
#
# # Read the documents
# med_details = collection_name.find({})
# # Print on the terminal
# for r in med_details:
#     print(r["common_name"])
# # Update one document
# update_data = collection_name.update_one({'medicine_id': 'RR000123456'}, {'$set': {'common_name': 'Paracetamol 500'}})
#
# # Delete one document
# delete_data = collection_name.delete_one({'medicine_id': 'RR000123456'})


def getImg(idMovie):
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


def getTitle(idMovie):
    url = "https://api.themoviedb.org/3/movie/%i?language=en-EN" % idMovie
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMmZiY2NjNzA0MmM4NjQ2ODNlZWFjYzIwNGI3NmFmZiIsInN1YiI6IjY0N2Q5MWU3Y2Y0YjhiMDBhODc4N2YxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mzdeeD2vVHgRNLkgO4z9h8GxzUMcPKLbE28bhuWihJg"
    }
    response = json.loads(requests.get(url, headers=headers).text)
    title = response["title"]
    return title


def home(request, page=1):
    url = "https://api.themoviedb.org/3/movie/changes?page=%i" % page
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMmZiY2NjNzA0MmM4NjQ2ODNlZWFjYzIwNGI3NmFmZiIsInN1YiI6IjY0N2Q5MWU3Y2Y0YjhiMDBhODc4N2YxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mzdeeD2vVHgRNLkgO4z9h8GxzUMcPKLbE28bhuWihJg"
    }
    response = json.loads(requests.get(url, headers=headers).text)
    listMovie = []
    for movie in response["results"]:
        listMovie.append({"title": getTitle(movie["id"]), "image": getImg(movie["id"])})
    return render(request, "movies.html", {
        "listMovie": listMovie
    })
