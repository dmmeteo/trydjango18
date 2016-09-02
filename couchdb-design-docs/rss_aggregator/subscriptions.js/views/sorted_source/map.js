function (doc) {
    if (doc.type == 'source') {
        emit (doc._id, [doc.title, doc.link, doc.read]);
    }
}