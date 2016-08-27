import django_couch

# Declare our couch database source
db = django_couch.db('db')

# Taken view, we're retrieving from couchdb
def response(view):
    return db.view('subscriptions/{}' .format(view)).rows
