"use strict";
var dream = dream || {};

// ############################################################################
// ############################################################################
dream.TeamCreator = function() {
    // Initialize team creator
};

// ############################################################################
// ############################################################################
$(document).ready(function() {
    // TODO: Move this into its own namespace
    $('#tbl-clubs').DataTable({
        serverSide: true, // Tell it I want to call the server
        processing: true, // Loading screen enable
        ajax: {
            url: dream.Context['team-creator-api'],
            type: 'POST',
            data: {'clubs-table': true},
            beforeSend: function( xhr ) {
                xhr.setRequestHeader('X-CSRFToken', dream.utils.getCookie('csrftoken'));
            }
        },
        columns: [
            // TODO: Configure columns width, add formatters
            { data: 'team_count' },
            { data: 'manager_name' },
            { data: 'club_name' },
            { data: 'country' },
            { data: 'created' },
            { data: 'actions' }
        ]
    });
});
