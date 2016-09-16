function (doc) {
    if (doc.type == 'source') {
        emit(doc.title, null);
    }
}