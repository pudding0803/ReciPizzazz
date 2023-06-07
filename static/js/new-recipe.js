$(document).ready(function () {
    $('#add-button').on('click', () => {
       $.ajax({
            url: '/add_recipe_row',
            type: 'GET',
            success: function (response) {
                $('#ingredients').append(response);
            }
        });
    });
});