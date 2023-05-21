$(document).ready(function () {
    $('.notification .delete').each(function () {
        const $delete = $(this);
        const $notification = $delete.parent();

        $delete.on('click', function () {
            $notification.remove();
        });
    });

    $('.notification').each(function () {
        const $notification = $(this);
        $notification.css('opacity', '0');
        setTimeout(function () {
           $notification.remove();
        }, 5000);
    });
});
