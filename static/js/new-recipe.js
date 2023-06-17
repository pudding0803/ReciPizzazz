$(document).ready(function () {
    $('#add-button').on('click', function () {
        $.ajax({
            url: '/add_recipe_row',
            type: 'GET',
            success: function (response) {
                $('#ingredients').append(response);
            }
        });
    });

    $(document).on('click', 'button.delete-button', function () {
        $(this).closest('div.row').remove();
    });

    $('form').on('submit', function (event) {
        event.preventDefault();
        $('#instructions').val(CKEDITOR.instances['instructions'].getData());
        const ingredients = [];
        $('.row').each(function () {
            ingredients.push({
                name: $(this).find('.name').val(),
                quantity: $(this).find('.quantity').val()
            });
        });
        const form = $(this);
        const data = new FormData(form[0]);
        data.append('ingredients', encodeURIComponent(JSON.stringify(ingredients)));
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: data,
            processData: false,
            contentType: false,
            success: function () {
                window.location.href = '/';
            }
        });
    });
});