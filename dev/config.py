import os

class Config():

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-never-known'


    def __repr__(self):
        return('ES CONFIG!')