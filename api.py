"""
Backend program for Capstone
"""
import os
from werkzeug.http import HTTP_STATUS_CODES

from flask import Flask, request, abort, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import setup_db, Movie, Actor, Movie_actor
from auth.auth import AuthError, requires_auth

MOVIES_PER_PAGE = 10


# def create_app(test_config=None):
#     # create and configure the app

app = Flask(__name__)
setup_db(app)
CORS(app)

    # @app.after_request
    # def after_request(response):
    #     response.headers.add(
    #         "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    #     )
    #     response.headers.add(
    #         "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
    #     )
    #     return response

"""
List actors
"""

@app.route("/actors", methods=["GET"])
# @requires_auth('get:actors')
def retrieve_actors():
    try:
        selection = Actor.query.order_by(Actor.id).paginate(per_page=MOVIES_PER_PAGE)
        actors = [actor.format() for actor in selection.items]
        if len(actors) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "actors": actors,
                "total_actors": len(Actor.query.all())                    
            }
        )
    except Exception as error:
        print(error)
        abort(404)

"""
List Movies
"""
@app.route("/movies", methods=["GET"])
# @requires_auth('get:movies')
def retrieve_movies():
    try:
        selection = Movie.query.order_by(Movie.id).paginate(per_page=MOVIES_PER_PAGE)
        movies = [movie.format() for movie in selection.items]
        if len(movies) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "movies": movies,
                "total_movies": len(Movie.query.all())                    
            }
        )
    except Exception as error:
        print(error)
        abort(404)
"""
Delete Movie
"""
@app.route("/movies/<int:movie_id>", methods=["DELETE"])
@requires_auth('delete:movies')
def delete_movie(payload,movie_id):

    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        movie.delete()

        return jsonify(
            {
                "success": True,
                "deleted movie": [movie.format()]
            }
        )
    except Exception as error:
        print(error)
        abort(404)

"""
Delete Actor
"""
@app.route("/actors/<int:actor_id>", methods=["DELETE"])
@requires_auth('delete:actors')
def delete_actor(payload,actor_id):

    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        actor.delete()

        return jsonify(
            {
                "success": True,
                "deleted actor": [actor.format()]
            }
        )
    except Exception as error:
        print(error)
        abort(404)

"""
Post movies
"""
@app.route("/movies", methods=["POST"])
@requires_auth('post:movies')
def add_movies(payload):

    body = request.get_json()
    new_title = body.get("title", None)
    new_releasedt = body.get("release_date", None)

    try:
        if (new_title is None):
            abort(400)

        movie = Movie(title=new_title, release_date=new_releasedt)
        movie.insert()

        return jsonify(
            {
                "success": True,
                "created": movie.id,
                "title": new_title
            }
        )

    except Exception as error:
        print(error)
        abort(400)

"""
Post actors
"""
@app.route("/actors", methods=["POST"])
@requires_auth('post:actors')
def add_actors(payload):

    body = request.get_json()
    new_name = body.get("name", None)
    new_age = body.get("age", None)
    new_gender = body.get("gender", None)

    try:
        if (new_name is None):
            abort(400)

        actor = Actor(name=new_name, age=new_age, gend=new_gender)
        actor.insert()

        return jsonify(
            {
                "success": True,
                "created": actor.id,
                "actor name": new_name
            }
        )

    except Exception as error:
        print(error)
        abort(400)

"""
Update actors information
"""
@app.route("/actors/<int:actor_id>", methods=["PATCH"])
@requires_auth('patch:actors')
def patch_drinks(payload,actor_id):
    try:

        body = request.get_json()
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)
                    
        actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
        if actor:
            if new_age:
                actor.age = new_age
            if new_gender:
                actor.gend = new_gender
            actor.update()
        
            return jsonify({
                "success": True,
                "Updated details": [actor.format()]
            })
        else:
            abort(404)
    except Exception as error:
        print(error)
        abort(422)

"""
Update movies information
"""
@app.route("/movies/<int:movie_id>", methods=["PATCH"])
@requires_auth('patch:movies')
def patch_movies(payload,movie_id):
    try:

        body = request.get_json()
        new_rdate = body.get("reldate", None)
                    
        movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
        if movie:
            if new_rdate:
                movie.release_date = new_rdate
            movie.update()
        
            return jsonify({
                "success": True,
                "Updated details": [movie.format()]
            })
        else:
            abort(404)
    except Exception as error:
        print(error)
        abort(422)

"""
Update movies_actor information
"""
@app.route("/movieactors", methods=["POST"])
@requires_auth('post:movieactors')
def movie_actor(payload):
    body = request.get_json()
    new_movieid = body.get("movie_id", None)
    new_actorid = body.get("actor_id", None)

    try:
        if (new_movieid is None or new_actorid is None):
            abort(400)

        movie_actor = Movie_actor(movie_id=new_movieid, actor_id=new_actorid)
        movie_actor.insert()
        movie = Movie.query.filter(Movie.id==new_movieid).one_or_none()
        actor = Actor.query.filter(Actor.id==new_actorid).one_or_none()

        return jsonify(
            {
                "success": True,
                "Movie details": [movie.format()],
                "Actor in the movie": [actor.format()]
            }
        )

    except Exception as error:
        print(error)
        abort(400)

"""x
Error handlers for all expected errors
including 404 and 422.
"""

@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

@app.errorhandler(405)
def not_found(error):
    return (
        jsonify({"success": False, "error": 405, "message": "method not allowed"}),
        405,
    )

@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )

@app.errorhandler(AuthError)
def handle_auth_error(err):
    response = {
        "message": HTTP_STATUS_CODES.get(err.status_code),
        "description": err.error,
    }
    return response, err.status_code