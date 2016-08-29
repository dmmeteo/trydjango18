function (doc) {
    if (doc.type == 'source') {
        emit (doc.date, [doc.title, doc.link, doc.user, doc.read]);
    }
}
