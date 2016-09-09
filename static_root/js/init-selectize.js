$(document).ready(function() {
    $('#id_item').selectize();
    $('#id_action').selectize();
    $('#id_sources').selectize({
        plugins: ['remove_button']
    });
});