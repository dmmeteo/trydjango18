function (doc) {
    if (doc.type == 'parsed') {
        emit (doc.title, null);
    }
}