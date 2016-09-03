function (doc) {
    if (doc.type == 'filter') {
        emit(doc._id, {"title": doc.title, "item": doc.item, "action": doc.action, "word": doc.word, "link": doc.link});
    }
}