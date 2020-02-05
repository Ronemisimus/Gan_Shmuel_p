import os

class Config(object):
    uri_string ='mysql://{0}:{1}@{2}/{3}'.format(os.environ["DB_USER"], os.environ["DB_PASSWORD"], os.environ["DB_HOST_NAME"], os.environ["DB_DATABASE"])
    SQLALCHEMY_DATABASE_URI = uri_string
    SQLALCHEMY_TRACK_MODIFICATIONS = False