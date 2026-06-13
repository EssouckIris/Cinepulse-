from flask import Blueprint, jsonify, request
from Model.recommend_gcn import recommend_by_user, recommend_by_title

recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route("/recommend/<int:user_index>", methods=["GET"])
def get_recommendations(user_index):
    recommendations = recommend_by_user(user_index)
    return jsonify({"recommended_movies": recommendations})

@recommendation_bp.route("/recommend_by_name", methods=["GET"])
def search_by_name():
    title = request.args.get("title", "")
    results = recommend_by_title(title)
    return jsonify({"recommended_movies": results})