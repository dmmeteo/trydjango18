function (doc) {
    if (doc.type == 'source') {
        emit (doc.user, [doc.title, doc.link, doc.read]);
    }
}