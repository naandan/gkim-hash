$(document).ready(function() {
    function toggleInputFields(fieldset, checkboxSelector, excludeSelector) {
        const isChecked = fieldset.find(checkboxSelector).prop('checked');
        fieldset.find('input:not(' + checkboxSelector + '):not(' + excludeSelector + '), select').prop('readonly', !isChecked)
    }
    function handleCheckboxChange(checkboxSelector, excludeSelector) {
        $(checkboxSelector).each(function() {
            toggleInputFields($(this).closest('fieldset'), checkboxSelector, excludeSelector);
            $(this).change(function() {
                toggleInputFields($(this).closest('fieldset'), checkboxSelector, excludeSelector);
            });
        });
    }

    handleCheckboxChange('.field-is_employee input[type="checkbox"]', '');
    handleCheckboxChange('.field-is_servant_of_god #id_ServantOfGod-0-is_servant_of_god', '');
    handleCheckboxChange('.field-is_congregation input[type="checkbox"]', '');
});
