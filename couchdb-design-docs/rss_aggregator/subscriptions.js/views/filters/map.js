function (doc) {
    if (doc.type == 'filter') {
        emit(doc.user, {"title": doc.title});
    }
}