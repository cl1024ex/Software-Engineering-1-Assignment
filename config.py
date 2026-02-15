import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b"r\xfaN\xa5\xdd\xa2at'\xf6J\xadM\xfa\xaa\x83"
    # to create secret key python -c "import os; print(os.urandom(16))"

    MONGODB_SETTINGS = {'db': 'UTA_Enrollment'}
    # 'host': 'mongodb://localhost:27017/UTA_Enrollment'
