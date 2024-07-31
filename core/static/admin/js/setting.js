$(document).ready(function() {
    if ($('.field-allow_edit').length) {
        var newContent = $('<div class="container flex-column mb-3"><h1 class="fs-2 fw-bold">Kunci Data Jemaat</h1><p>Jika diaktifkan Jemaat tidak dapat merubah data secara mandiri</p></div>');
        
        $('.field-allow_edit').prepend(newContent);
    }
});
