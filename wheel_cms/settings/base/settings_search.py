from .util import get_env_variable

HAYSTACK_SITECONF = 'wheelcms_axle.search_sites'

HAYSTACK_SEARCH_ENGINE = "solr"

HAYSTACK_SOLR_URL = get_env_variable('SOLR_URL', 'http://127.0.0.1:8983/solr')
HAYSTACK_INCLUDE_SPELLING = True

# 2.x config
#HAYSTACK_CONNECTIONS = {
#
#    'default': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr'
#        # ...or for multicore...
#        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
#    },
#}
