# RSS aggregator with others things.

## Prerequisites

Here's all what you need for launch this app.

### requirements for pip
By means terminal lauch a command: _pip install -r dep.txt_

### PostgresSQL dump
Just import exportdb.psql by means a command in termianl (_psql base < exportdb.pgsql_), and replace in exportdb.pgsql "vkrylasov" to your user name.

### CouchDB view
You can import all needed couchdb views by means command: (_./manage.py couch restore -n db -p couchdb-design-docs/rss_aggregator -r -f_)
