DEFAULT_DB = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'wheel.db'
}
TEST_DB = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory:///'
}

DATABASES = {
    'default': DEFAULT_DB
}
