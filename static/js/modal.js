$(document).ready(function() {
    // Functions to open and close a modal
    function openModal($el) {
        $el.addClass('is-active');
    }

    function closeModal($el) {
        $el.removeClass('is-active');
    }

    function closeAllModals() {
        $('.modal').each(function() {
            closeModal($(this));
        });
    }

    // Add a click event on buttons to open a specific modal
    $('.js-modal-trigger').click(function() {
        const modal = $(this).data('target');
        const $target = $('#' + modal);
        const $adjust = $('input.adjust').filter(function() {
            return $(this).val() !== '';
        }).first();
        const $quantity = $adjust.closest('.field').find('.quantity');
        $('#adjust-ratio').text(`${$adjust.val()} / ${$quantity.val()}`);
        openModal($target);
    });

    // Add a click event on various child elements to close the parent modal
    $('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button').click(function() {
        const $target = $(this).closest('.modal');

        closeModal($target);
    });

    // Add a keyboard event to close all modals
    $(document).keydown(function(event) {
        if (event.key === 'Escape') { // Escape key
            closeAllModals();
        }
    });
});
