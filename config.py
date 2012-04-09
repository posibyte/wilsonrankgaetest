from webapp2_extras import sessions_ndb
from secret_keys import SESSION_KEY

config = {}

# Secret Keys
config['webapp2_extras.sessions'] = {
    'secret_key' : SESSION_KEY,
    'factory' : sessions_ndb.DatastoreSessionFactory,
}