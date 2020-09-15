$('.ui.basic.modal')
    .modal('attach events', '.quit', 'show')
;

$('.ui.modal.add-bot')
    .modal('setting', 'closable', false)
    .modal('attach events', '.add', 'show')
;

$('.ui.modal.user-settings')
    .modal('attach events', '.user-settings', 'show')
;
