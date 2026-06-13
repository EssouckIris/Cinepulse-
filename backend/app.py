import sys
import os

from flask_cors import CORS

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

from flask import Flask, jsonify
from routes.recommendation_routes import (recommendation_bp)
from config import Config
app= Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.register_blueprint(recommendation_bp)


@app.route("/")
def home():
    return {"message":"API Movie Recommender"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)