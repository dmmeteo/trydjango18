# RSS aggregator with others things.

## Prerequisites

Here's all what you need for launch this app.

### requirements for pip
By means terminal lauch a command: _pip install -r dep.txt_

### PostgresSQL dump
Just import exportdb.psql by means a command in termianl (_psql -U <username> -d <dbname> -1 -f exportdb.pgsql_)

### CouchDB view
```javascript
function (doc) {
    if (doc.type == 'source') {
        emit (doc.date, [doc.title, doc.link, doc.user, doc.read]);
    }
}
```
