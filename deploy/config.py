import os

class Config():

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-never-know'

    def __repr__(self):
        return('CONFIG')