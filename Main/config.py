import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "adsdwarawf"
    MONGO_URI = os.environ.get("MONGODB_CONNSTRING")
    SECRET_API_KEY = "BASIC_KEY"