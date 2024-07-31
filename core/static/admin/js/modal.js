$(document).ready(function() {
    const $btnClicked = $('#btn-registrasi-rfid');

    if ($btnClicked.length) {
        $('.addlink').hide();

        $btnClicked.click(function() {
            const modalEl = $('#myModal');

            if (modalEl.length) {
                const modal = new bootstrap.Modal(modalEl[0]); 
                modal.show();

                modalEl.on('hidden.bs.modal', function() {
                    location.reload();
                });

                initializeSelect2();
            }
        });
    }

    $(document).on('htmx:afterSwap', function(event) {
        if (event.detail.target.id === 'modal-content') {
            if (event.detail.xhr.status === 200) {
                initializeSelect2();    
            } else{
                initializeSelect2();  
            }
        }
    });

    function initializeSelect2() {
        $('#id_masteruser').select2({
            dropdownParent: $('#myModal'),
        });

        $('.select2-container').addClass('d-flex flex-column w-100');
        $('.select2-selection--single').attr('style', 'height: 38px !important; display: flex; align-items: center;');

        $('#id_masteruser').on('select2:open', function(e) {
            $('#select2-id_masteruser-results').addClass('d-flex flex-column');
        });
    }
});