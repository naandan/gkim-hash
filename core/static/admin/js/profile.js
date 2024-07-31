$(document).ready(function() {
    const labelProfile = $('label[for="id_profile_photo"]');
    const inputProfile = $('#id_profile_photo');
    const errorProfile = $('.field-profile_photo .errorlist');
    const cloneInput = inputProfile.clone();
    const image = $('#img-preview');
    
    labelProfile.attr('for', 'id_profile_photo_cloned');
    labelProfile.text('Ubah Foto Profil');
    cloneInput.attr({
      'name': 'profile_photo_cloned',
      'id': 'id_profile_photo_cloned'
    });

    $('.field-profile_photo').hide();

    const errorText = errorProfile.find('li').text();
    const errorElement = errorText ? `<div class="position-fixed top-0 end-0 p-3" style="z-index: 11">
      <div id="errorToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" class="text-danger" viewBox="0 0 24 24">
            <path fill="currentColor" d="M12 17q.425 0 .713-.288T13 16t-.288-.712T12 15t-.712.288T11 16t.288.713T12 17m-1-4h2V7h-2zm1 9q-2.075 0-3.9-.788t-3.175-2.137T2.788 15.9T2 12t.788-3.9t2.137-3.175T8.1 2.788T12 2t3.9.788t3.175 2.137T21.213 8.1T22 12t-.788 3.9t-2.137 3.175t-3.175 2.138T12 22" />
          </svg>
          <strong class="me-auto">Terjadi kesalahan</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          ${errorText}
        </div>
      </div>
    </div>` : '';
    
    $('#clone-input').append(labelProfile, cloneInput, errorElement);
    if (errorText) {
      const toast = new bootstrap.Toast(document.getElementById('errorToast'));
      toast.show();
    }
    const copyFileValue = (source) => {
      const files = source.files;
      if (files.length > 0) {
        const file = files[0];
        const clonedFile = new File([file.slice()], file.name, { type: file.type });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(clonedFile);
        inputProfile[0].files = dataTransfer.files;
      }
    };
    
    const handleInputChange = (event) => {
      const target = event.target;
      if (target.files.length) {
        const src = URL.createObjectURL(target.files[0]);
        image.attr('src', src);
      }
      copyFileValue(target);
    };
  
    inputProfile.on('change', handleInputChange);
    cloneInput.on('change', handleInputChange);
});

var divElements = document.querySelectorAll('div.col-md-placeholder');
divElements.forEach(function(div) {
  var fieldCount = div.getAttribute('data-field-count');
  var columnWidth = 12 / fieldCount;
  div.classList.add('col-md-' + columnWidth);
});