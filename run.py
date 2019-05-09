from flask import Flask, render_template, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from flask_pymongo import PyMongo
import re
import random
from gevent.pywsgi import WSGIServer


app = Flask(__name__,
static_folder = "./dist/static",
template_folder="./dist")
app.config["MONGO_URI"] = "mongodb://localhost:27017/movies"
mongo = PyMongo(app)
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


# 电影列表相关的API
class GetPage(Resource):
    def get(self, page):
        pageSize = 10
        skip = pageSize * (page - 1)
        pageRecord = mongo.db.films.find()
        countMovie = pageRecord.count()
        pageRecord = pageRecord.limit(pageSize).skip(skip)
        return {'movies': list(pageRecord), 'count': countMovie}

# 电影详情页相关的API
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

# 排行榜相关的API
class GetGenres(Resource):
    def get(self):
        genres = mongo.db.films.find().distinct('genres')
        genres = list(genres)
        genres.remove('')
        return genres
class GetBoarding(Resource):
    def get(self, genre):
        movies = mongo.db.films.find({'genres': genre}, {'title': 1}).sort([("rating.average", -1)]).limit(10)
        return list(movies)
class GetTotalBoarding(Resource):
    def get(self):
        movies = mongo.db.films.find({}, {'title': 1}).sort([("rating.average", -1)]).limit(10)
        return list(movies)

# 搜索相关的API
class SearchTitle(Resource):
    def post(self):
        data = request.form
        title = data['title']
        page = int(data['page'])
        pageSize = 10
        skip = pageSize * (page - 1)
        rexExp = re.compile('.*' + title + '.*', re.IGNORECASE)
        movies = mongo.db.films.find({'title': rexExp})
        countMovie = movies.count()
        movies = movies.limit(pageSize).skip(skip)
        return {'movies': list(movies), 'count': countMovie}
class SearchCasts(Resource):
    def post(self):
        data = request.form
        name = data['casts']
        page = int(data['page'])
        pageSize = 10
        skip = pageSize * (page - 1)
        rexExp = re.compile('.*' + name + '.*', re.IGNORECASE)
        movies = mongo.db.films.find({'casts.name': rexExp})
        countMovie = movies.count()
        movies = movies.limit(pageSize).skip(skip)
        return {'movies': list(movies), 'count': countMovie}
class SearchDirectors(Resource):
    def post(self):
        data = request.form
        name = data['directors']
        page = int(data['page'])
        pageSize = 10
        skip = pageSize * (page - 1)
        rexExp = re.compile('.*' + name + '.*', re.IGNORECASE)
        movies = mongo.db.films.find({'directors.name': rexExp})
        countMovie = movies.count()
        movies = movies.limit(pageSize).skip(skip)
        return {'movies': list(movies), 'count': countMovie}
class SearchSummary(Resource):
    def post(self):
        data = request.form
        text = data['text']
        page = int(data['page'])
        pageSize = 10
        skip = pageSize * (page - 1)
        rexExp = re.compile('.*' + text + '.*', re.IGNORECASE)
        movies = mongo.db.films.find({'summary': rexExp})
        countMovie = movies.count()
        movies = movies.limit(pageSize).skip(skip)
        return {'movies': list(movies), 'count': countMovie}


api.add_resource(GetPage, '/api/page=<int:page>')
api.add_resource(GetCertainMovie, '/api/_id=<string:_id>')
api.add_resource(GetRandomMovies, '/api/random=<int:num>')
api.add_resource(GetGenres, '/api/genres')
api.add_resource(GetBoarding, '/api/genre=<string:genre>')
api.add_resource(GetTotalBoarding, '/api/genre')
api.add_resource(SearchTitle, '/api/title&page')
api.add_resource(SearchCasts, '/api/casts&page')
api.add_resource(SearchDirectors, '/api/directors&page')
api.add_resource(SearchSummary, '/api/summary&page')

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()