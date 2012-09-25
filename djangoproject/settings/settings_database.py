DEFAULT_DB = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'stracksite.db'
}
TEST_DB = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory:///'
}

DATABASES = {
    'default': DEFAULT_DB
}
