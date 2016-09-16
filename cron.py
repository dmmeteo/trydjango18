import os
import feedparser
import time
import django_couch
from django_couch import ResourceNotFound

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rss_aggregator.settings")

def cron_task():
    # Define a database source
    db = django_couch.db('db')

    # Define a view of couchdb
    view = db.view('subscriptions/filters').rows

    for filtern in view:
        # Catch up all documents that satisfied our couch view
        response = db.view('subscriptions/sorted_filter', key=filtern.id).rows

        # Save all filters into item's list
        values = {}
        for item in response:
            values.update(item.value)

        # Here we're saving parsed links of our sources.
        links = []
        for source in values['sources']:
            try:
                # We're parsing whole bunch of links that located in filter of user.
                links.append(feedparser.parse(db[source].link))
            except ResourceNotFound:
                pass

        # Deleted magic indexes
        for link in links:
            for parsed in link.entries:
                view = db.view('subscriptions/cron_view2', key=parsed.title)
                if not view:
                    data = {
                        "type": "parsed",
                        "filter_id": filtern.id,
                        "filter_name": filtern.value['title']
                    }
                    title, description, word = parsed.title.lower(), parsed.description.lower(), values['word'].lower()
                    val1, val2 = str(values['item']), str(values['action'])

                    # If word in title and item is title, and parsed is "contains",
                    # we'll write all matched values into parsed list
                    if word in title and ('title' in val1 and 'contains' in val2):
                        data.update(
                            {"title": parsed.title, "desc": parsed.description, "link": parsed.link}
                        )
                        db.create(data)
                        print "{} Successfully added into database. \n" .format(time.strftime("%Y/%m/%d, %H:%M:%S"))

                    # If word in description and item is title, and parsed is "contains",
                    # we'll write all matched values into parsed list
                    elif word in description and ('desc' in val1 and 'contains' in val2):
                        data.update(
                            {"title": parsed.title, "desc": parsed.description, "link": parsed.link}
                        )
                        db.create(data)
                        print "{} Successfully added into database. \n" .format(time.strftime("%Y/%m/%d, %H:%M:%S"))

                    # If word in title and item is title, and parsed is "don't contain",
                    # we'll write all matched values into parsed list
                    elif word not in title and ('title' in val1 and 'dc' in val2):
                        data.update(
                            {"title": parsed.title, "desc": parsed.description, "link": parsed.link}
                        )
                        db.create(data)
                        print "{} Successfully added into database. \n" .format(time.strftime("%Y/%m/%d, %H:%M:%S"))

                    # If word in description and item is title, and parsed is "don't contain",
                    # we'll write all matched values into parsed list
                    elif word not in description and ('desc' in val1 and 'dc' in val2):
                        data.update(
                            {"title": parsed.title, "desc": parsed.description, "link": parsed.link}
                        )
                        db.create(data)
                        print "{} Successfully added into database. \n" .format(time.strftime("%Y/%m/%d, %H:%M:%S"))
                else:
                    print "{} Parsed sources already exists. \n" .format(time.strftime("%Y/%m/%d, %H:%M:%S"))
    return 'You\'ve successully updated your feeds.'
