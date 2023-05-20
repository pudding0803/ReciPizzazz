$(document).ready(function () {
    $('.notification .delete').each(function () {
        const $delete = $(this);
        const $notification = $delete.parent();

        $delete.on('click', function () {
            $notification.remove();
        });
    });
});
