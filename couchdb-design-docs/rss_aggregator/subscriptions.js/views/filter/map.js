function (doc) {
    if (doc.type == 'filter') {
        emit (doc.user, [doc.title, doc.item, doc.action, doc.word, doc.link]);
    }
}