from flask import Blueprint, jsonify, request
from Model.recommend import recommend, recommend_by_name


# creation du Blueprint

recommendation_bp = Blueprint("recommendation", __name__)
@recommendation_bp.route("/recommend_by_name", methods=["GET"])

def search_by_name():
    title = request.args.get("title", "")
    results = recommend_by_name(title)
    return jsonify({"recommended_movies": results})
#route recommendations
@recommendation_bp.route("/recommend/<int:movie_index>", methods=["GET"])

def get_recommendations(movie_index):
    recommendations= recommend(movie_index)
    return jsonify({"recommended_movies": recommendations})