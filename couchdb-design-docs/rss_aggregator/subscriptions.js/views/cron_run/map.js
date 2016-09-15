function (doc) {
    if (doc.type == "parsed") {
        emit(doc.filter_id, {"name": doc.filter_name, "title": doc.title, "desc": doc.desc});
    }
}
