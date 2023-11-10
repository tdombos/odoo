odoo.define('website_form_helpdesk.form', function (require) {
'use strict';

var core = require('web.core');
var FormEditorRegistry = require('website.form_editor_registry');

var _t = core._t;

FormEditorRegistry.add('create_ticket', {
    formFields: [{
        type: 'char',
        modelRequired: true,
        name: 'name',
        string: 'Ticket Title',
    }, {
        type: 'email',
        fillWith: 'email',
        name: 'partner_email',
        string: 'Your Email',
    }, {
        type: 'char',
        name: 'description',
        string: 'Description',
    }],
    fields: [{
        name: 'team_id',
        type: 'many2one',
        relation: 'helpdesk.ticket.team',
        string: _t('Team'),
        createAction: 'helpdesk_mgmt.helpdesk_ticket_team_action',
    }],
});

});
