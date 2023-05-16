function parseFraction(fraction) {
    const parts = fraction.split('/').map(function(part) {
        return part.trim();
    });
    if (parts.length === 2) {
        const numerator = parseFloat(parts[0]);
        const denominator = parseFloat(parts[1]);
        if (!isNaN(numerator) && !isNaN(denominator) && denominator !== 0) {
            return numerator / denominator;
        }
    }
    return NaN;
}

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
        const $currentInput = $(this);
        const $currentRow = $currentInput.closest('div[id^="row-"]');
        $('#adjust-button').prop('disabled', !$currentInput.val());
        $('#ingredients > div').not($currentRow).each(function() {
            $(this).find('.adjust').prop('disabled', $currentInput.val());
        });
    });

    $(document).on('click', 'button.lock-button', function() {
        const $button = $(this);
        $button.parent().parent().toggleClass('has-background-danger-light');
        $.ajax({
            url: '/toggle_lock',
            type: 'GET',
            data: { locked: $button.data('state') === 'locked' },
            success: function(response) {
                $button.replaceWith(response);
            }
        });
    });

    $('#update-button').on('click', () => {
        $('#ingredients > div').each(function() {
            const $quantity = $(this).find('.quantity');
            const $lock = $(this).find('.lock-button');
            if ($lock.data('state') === 'unlocked') {
                const adjustedValue = $quantity.val() * parseFraction($('#adjust-ratio').text());
                $quantity.val(+adjustedValue.toFixed(2));
            }
            $(this).find('.adjust').prop('disabled', false);
        });
        $('input.adjust').filter(function() {
            return $(this).val() !== '';
        }).first().val('');
        $('#adjust-button').prop('disabled', true);
    });
});