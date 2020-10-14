$('.ui.basic.modal')
    .modal('attach events', '.quit', 'show')
;

$('.ui.modal.add-bot')
    .modal('setting', 'closable', false)
    .modal('attach events', '.add', 'show')
;

$('.ui.modal.user-settings')
    .modal('attach events', '.edit', 'show')
;

$('.ui.modal.checkout')
    .modal('attach events', '.buymodal', 'show')
;

$('.ui.modal.buy-plan')
    .modal('attach events', '.buyplanmodal', 'show')
;