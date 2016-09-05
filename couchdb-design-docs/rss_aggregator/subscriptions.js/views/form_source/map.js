function (doc) {
    if (doc.type == 'source') {
        emit(doc._id, {"title": doc.title, "link": doc.link});
    }
}