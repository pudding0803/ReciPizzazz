$(document).ready(function () {

    $(document).on('click', '#like-button', function() {
        const $button = $(this);
        $.ajax({
            url: '/toggle_like',
            type: 'GET',
            data: {
                token: window.location.pathname.split('/').pop(),
                liked: $button.data('state') === 'liked',
                like_count: $('#like-count').text()
            },
            success: function(response) {
                $button.replaceWith(response);
            }
        });
    });

    $(document).on('click', '#mark-button', function() {
        const $button = $(this);
        $.ajax({
            url: '/toggle_mark',
            type: 'GET',
            data: {
                token: window.location.pathname.split('/').pop(),
                marked: $button.data('state') === 'marked'
            },
            success: function(response) {
                $button.replaceWith(response);
            }
        });
    });
});