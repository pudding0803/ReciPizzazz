$(document).ready(function () {
    $(document).on('click', '#follow-button', function() {
        const $button = $(this);
        $.ajax({
            url: '/toggle_follow',
            type: 'GET',
            data: {
                followed_name: window.location.pathname.split('/').pop(),
                following: $button.data('following')
            },
            success: function(response) {
                $button.replaceWith(response);
                $('#follower-count').text(function() {
                    return parseInt($(this).text(), 10) + ($button.data('following') ? -1 : 1);
                });
            }
        });
    });
});