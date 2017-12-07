from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
from engine import RecommendationEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request

@main.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings = recommendation_engine.get_top_ratings(user_id,count)
    return json.dumps(top_ratings)
 
@main.route("/ratings", methods = ["POST"])
def add_ratings():
    # get the ratings from the Flask POST request object
    ratings_list = request.get_json().get('ratings')

    # create a list with the format required by the engine (user_id, game_id, rating)
    ratings = map(lambda x: (1, int(x['id']), float(x['rating'])), ratings_list)
    # add them to the model using then engine API
    recommendation_engine.add_ratings(ratings)
    top_ratings = recommendation_engine.get_top_ratings(user_id,10)
 
    return json.dumps(top_ratings)
 
 
def create_app(spark_context, dataset_path):
    global recommendation_engine 

    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
