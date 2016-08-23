# RSS aggregator with others things.

## Prerequisites

Here's all what you need for launch this app.

### requirements for pip (_pip install -r dep.txt_)
couchdb-python-curl==1.1.6
Django==1.8
django-allauth==0.26.1
django-couch-utils==1.5.5
django-crispy-forms==1.6.0
django-disqus==0.5
django-registration-redux==1.4
funcsigs==1.0.2
mock==1.3.0
oauthlib==1.1.2
pbr==1.10.0
pip-autoremove==0.9.0
psycopg2==2.6.2
pycurl==7.43.0
python-openid==2.2.5
requests==2.11.0
requests-oauthlib==0.6.2
six==1.10.0

### PostgresSQL dump
Just import exportdb.psql by means a command in termianl (psql -U <username> -d <dbname> -1 -f exportdb.pgsql)

### CouchDB view
```javascript
function (doc) {
    if (doc.type == 'source') {
        emit (doc.date, [doc.title, doc.link, doc.user, doc.read]);
    }
}
```
