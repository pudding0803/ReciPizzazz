$(document).ready(function () {
    $('#add-button').click(function () {
        $.ajax({
            url: '/add_row',
            type: 'GET',
            data: { row: $('#ingredients').children().length },
            success: function (response) {
                $('#ingredients').append(response);
            }
        });
    });
});