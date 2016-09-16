function (doc) {
    if (doc.type == "parsed") {
        emit (doc.pub, null);
    }
}