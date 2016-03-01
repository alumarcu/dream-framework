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
    $(document).foundation(); // Initializes foundation

     // Balance equalizer inside reveal
$(document).on('opened.fndtn.reveal', '[data-reveal]', function () {
    $(document).foundation('equalizer');
});

    // TODO: Move this into its own namespace
    var clubs_table = $('#tbl-clubs').DataTable({
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
            { data: null, width: '1em', orderable: false, className: 'select-checkbox', defaultContent: '' },
            { data: 'team_count', className: 'dt-center', width: '2em' },
            { data: 'manager_name', width: '6em' },
            { data: 'club_name', width: '6em' },
            { data: 'country', width: '3em' },
            { data: 'created', width: '4em' },
            { data: 'actions', width: '6em' }
        ],
        select: {
            style: 'multi',
            selector: 'td:first-child'
        }
    });

    //$('#btn-new-club').click(function() {
    //    $('#modal-new-club').foundation('reveal', 'open');
    //});


});
/**
//columnDefs: [ {
//    orderable: false,
//    className: 'select-checkbox',
//    defaultContent: '',
//    targets: 0
//} ],
 *
 *
     $('#tbl-clubs tbody').on('click', 'tr', function () {
        var id = this.id;
        var index = $.inArray(id, selected);

        if ( index === -1 ) {
            selected.push( id );
        } else {
            selected.splice( index, 1 );
        }

        $(this).toggleClass('selected');
    } );

 var selected = [];
$(document).ready(function() {
    var selected = [];

    $("#example").DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": "scripts/ids-arrays.php",
        "rowCallback": function( row, data ) {
            if ( $.inArray(data.DT_RowId, selected) !== -1 ) {
                $(row).addClass('selected');
            }
        }
    });

    $('#example tbody').on('click', 'tr', function () {
        var id = this.id;
        var index = $.inArray(id, selected);

        if ( index === -1 ) {
            selected.push( id );
        } else {
            selected.splice( index, 1 );
        }

        $(this).toggleClass('selected');
    } );
} );
 */