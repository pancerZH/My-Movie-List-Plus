from flask import Flask, render_template, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from flask_pymongo import PyMongo
import re
import random


app = Flask(__name__,
static_folder = "./dist/static",
template_folder="./dist")
app.config["MONGO_URI"] = "mongodb://localhost:27017/movies"
mongo = PyMongo(app)
api = Api(app)


class GetPage(Resource):
    def get(self, page):
        pageSize = 10
        skip = pageSize * (page - 1)
        pageRecord = mongo.db.films.find().limit(pageSize).skip(skip)
        return list(pageRecord)
class GetMovieCount(Resource):
    def get(self):
        countMovie = mongo.db.films.count()
        return countMovie
class GetCertainMovie(Resource):
    def get(self, _id):
        movie = mongo.db.films.find({'_id': _id})
        return list(movie)
class GetRandomMovies(Resource):
    def get(self, num):
        countMovie = mongo.db.films.count()
        limit = int(countMovie / num)
        page = random.randint(1, limit)
        skip = num * (page - 1)
        pageRecord = mongo.db.films.find({}, {'poster': 1, 'title': 1, '_id': 1}).limit(num).skip(skip)
        return list(pageRecord)
class GetGenres(Resource):
    def get(self):
        genres = mongo.db.films.find().distinct('genres')
        genres = list(genres)
        genres.remove('')
        return genres
class SearchTitle(Resource):
    def get(self, title):
        rexExp = re.compile('.*' + title + '.*', re.IGNORECASE)
        movies = mongo.db.films.find({'title': rexExp})
        return list(movies)
class SearchCasts(Resource):
    def get(self, name):
        rexExp = re.compile('.*' + name + '.*', re.IGNORECASE)
        movies = mongo.db.films.find({'casts.name': rexExp})
        return list(movies)
class SearchDirectors(Resource):
    def get(self, name):
        rexExp = re.compile('.*' + name + '.*', re.IGNORECASE)
        movies = mongo.db.films.find({'directors.name': rexExp})
        return list(movies)
class SearchSummary(Resource):
    def get(self, text):
        rexExp = re.compile('.*' + text + '.*', re.IGNORECASE)
        movies = mongo.db.films.find({'summary': rexExp})
        return list(movies)


api.add_resource(GetPage, '/api/page=<int:page>')
api.add_resource(GetMovieCount, '/api/movieCount')
api.add_resource(GetCertainMovie, '/api/_id=<string:_id>')
api.add_resource(GetRandomMovies, '/api/random=<int:num>')
api.add_resource(GetGenres, '/api/genres')
api.add_resource(SearchTitle, '/api/title=<string:title>')
api.add_resource(SearchCasts, '/api/casts=<string:name>')
api.add_resource(SearchDirectors, '/api/directors=<string:name>')
api.add_resource(SearchSummary, '/api/summary=<string:text>')

if __name__ == '__main__':
    app.run(debug=True)