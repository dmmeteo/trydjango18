function (doc) {
    if (doc.type == 'source') {
        emit(doc.user, {"title": doc.title, "link": doc.link, "read": doc.read});
    }
}