function (doc) {
    if (doc.type == 'filter') {
        emit (doc._id, [doc.title, doc.item, doc.action, doc.word, doc.link]);
    }
}