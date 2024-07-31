if (document.querySelector('#template-dummy_field-container')){
    document.body.addEventListener('htmx:configRequest', (event) => {
            event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
        });
    document.body.addEventListener('htmx:afterRequest', (event) => {
        response = JSON.parse(event.detail.xhr.response);
        if (response.success) {
            Swal.fire('Deleted!', response.message + '' + response.image_name , 'success');
            htmx.trigger(this, 'confirmed');
            const imageContainer = document.querySelector(`.container-images img[alt="${response.image_name}"]`).closest('.container-images');
            imageContainer.remove();
        }
        else {
            Swal.fire('Error',  response.message + response.image_name, 'error');
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    dateClass = [".vDateField", "#id_check_in_0", "#id_check_out_0", ".dateFlatpickrInput"];
    timeClass = [".vTimeField", "#id_check_in_1", "#id_check_out_1", ".timeFlatpickrInput"];

    function initializeFlatpickr() {
        dateClass.forEach(element => {
            $(element).flatpickr({
                dateFormat: "d-m-Y",
            })
        })

        timeClass.forEach(element => {
            $(element).flatpickr({
                enableTime: true,
                noCalendar: true,
                dateFormat: "H:i",
                time_24hr: true
            })
        })
        $('.DateFlatpickrInput').removeAttr('size');
        
        $('.InlineDateFlatpickrInput').removeAttr('readonly');
        $('.InlineDateFlatpickrInput').removeAttr('size');
        $('.InlineDateFlatpickrInput').css('cursor', 'pointer');
        $('.InlineDateFlatpickrInput').attr('autocomplete', 'off');

        $('[id$="check_in_0"], [id$="check_out_0"]').addClass('dateFlatpickrInput');
        $('[id$="check_in_1"], [id$="check_out_1"]').addClass('timeFlatpickrInput');
    }

    initializeFlatpickr();

    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1) {
                    const addedElement = $(node);

                    const needsDateInitialization = addedElement.find(dateClass.join(', ')).length > 0;
                    const needsTimeInitialization = addedElement.find(timeClass.join(', ')).length > 0;

                    if (needsDateInitialization || needsTimeInitialization) {
                        initializeFlatpickr();
                    }
                }
            });
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
