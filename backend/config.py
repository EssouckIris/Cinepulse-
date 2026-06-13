import os 

class Config:
    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )
    
    DEBUG = True
    SECRET_KEY = "movie_recommender_secret"