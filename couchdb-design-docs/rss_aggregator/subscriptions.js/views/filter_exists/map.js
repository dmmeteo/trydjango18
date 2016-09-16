function (doc) {
    if (doc.type == 'filter') {
        emit (doc.title, doc._id);
    }
}