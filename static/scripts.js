$(document).ready(function () {
    $('#add-button').on('click', () => {
        $.ajax({
            url: '/add_row',
            type: 'GET',
            data: { row: $('#ingredients').children().length },
            success: function (response) {
                $('#ingredients').append(response);
            }
        });
    });

    $('#ingredients').on('input', '.adjust', function() {
        const currentInput = $(this);
        const currentRow = currentInput.closest('div[id^="row-"]');
        $('#adjust-button').prop('disabled', !currentInput.val());
        $('#ingredients > div').not(currentRow).each(function() {
            $(this).find('.adjust').prop('disabled', currentInput.val());
        });
    });

    $('#update-button').on('click', () => {
        const adjust = $('input.adjust').filter(function() {
            return $(this).val() !== '';
        }).first().val();
        console.log(adjust);
    });
});