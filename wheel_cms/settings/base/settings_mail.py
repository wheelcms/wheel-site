from .util import get_env_variable

if get_env_variable('USE_POSTMARK', False):
    MAIL_SENDER = get_env_variable('POSTMARK_SENDER')
    POSTMARK_API_KEY = get_env_variable('POSTMARK_API_KEY', '')
    POSTMARK_SENDER = MAIL_SENDER
    EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'

    DEFAULT_FROM_EMAIL = MAIL_SENDER
else:
    EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS', False)
    EMAIL_HOST = get_env_variable('EMAIL_HOST', 'localhost')
    EMAIL_PORT = int(get_env_variable('EMAIL_PORT', 25))
    EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER', None)
    EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD', None)
