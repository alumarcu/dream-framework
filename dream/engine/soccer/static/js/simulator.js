"use strict";
var dream = dream || {};

// ############################################################################
// ############################################################################
/**
 * Canvas class
 * @param elementId
 * @constructor
 */
dream.Canvas = function(elementId) {
    // Perform GET call to fetch board settings
    this.canvas = document.getElementById(elementId); // TODO: Throw error if nothing is found
    this.context = this.canvas.getContext('2d');
};

// TODO: can you make it work without having these as static props ??
dream.Canvas.settings = {};
dream.Canvas.initd = false;

/**
 * Get server side setup data to initialize the canvas
 */
dream.Canvas.prototype.initialize = function() {
    $.ajax({
        url: dream.Context['simulator-api'],
        method: 'POST',
        data: {'setup': true},
        dataType: 'json',
        success: function(data) {
            dream.Canvas.settings = data['setup-data'];
            dream.Canvas.initd = true;
            console.log("OK - canvas initialized");
        },
        beforeSend: dream.utils.setCsrfToken()
    });
};

/**
 * Calls the method to draw the board using board state data
 * @param board_state
 */
dream.Canvas.prototype.load_board = function(board_state) {
    console.log("Loading Board");
    if (dream.Canvas.initd) {
        this.draw_board(board_state);
    }
};

/**
 * Draws the board
 * @param board_data
 */
dream.Canvas.prototype.draw_board = function(board_data) {
    var grid_width, grid_length,
        canvas_width, canvas_length,
        unit_of_width, unit_of_length,
        x, y, i, player_coordinates, ball_coordinates;

    grid_width = dream.Canvas.settings['grid_width'];
    grid_length = dream.Canvas.settings['grid_length'];

    canvas_width = this.canvas.width;
    canvas_length = this.canvas.height;

    this.context.strokeStyle = '#2F522E';

    unit_of_width = canvas_length / grid_length;
    unit_of_length = canvas_width / grid_width;

    // Clear the canvas of previous drawings
    this.context.clearRect(0, 0, canvas_width, canvas_length);

    x = 0; y = 0;

    // draws all horizontal lines on the canvas
    for (i = 0; i < grid_length; i++) {
        y = i * unit_of_width;

        this.context.moveTo(x, y + 0.5);
        this.context.lineTo(canvas_width, y + 0.5);
        this.context.stroke();
    }

    // draws all vertical lines on the canvas
    y = 0;
    for (i = 0; i < grid_width; i++) {
        x = i * unit_of_length;

        this.context.moveTo(x, y + 0.5);
        this.context.lineTo(x, canvas_length + 0.5);
        this.context.stroke();
    }

    player_coordinates = board_data['player_coordinates'];
    ball_coordinates = board_data['ball_coordinates'];

    // TODO: Optimized and specialized methods for drawing

    // draw players
    this.context.lineWidth = 3;
    for (i = 0; i < player_coordinates.length; i++) {
        var coords = player_coordinates[i];
        x = coords[0];
        y = coords[1];

        this.context.beginPath();
        this.context.strokeStyle = '#000000';
        this.context.arc(x * unit_of_length, y * unit_of_width, 4, 0, 2 * Math.PI);
        this.context.stroke();
    }
    this.context.lineWidth = 1;

    // draw ball
    this.context.beginPath();
    //this.context.strokeStyle = '#000000';

    this.context.fillStyle = '#FF0000';
    this.context.arc(ball_coordinates[0] * unit_of_length, ball_coordinates[1] * unit_of_width, 4, 0, 2 * Math.PI);
    //this.context.stroke();
    this.context.fill();
};

// ############################################################################
// ############################################################################
dream.Simulator = function() {
    // Initialize simulator
};

/**
 * Renders the list of ticks into the user interface
 * @param ticks_list
 */
dream.Simulator.load_ticks = function(ticks_list) {
    var htmlHead, table = $('#game-ticks');
    // TODO: Can be done in a slightly better way; but MUST BE DONE WITHOUT any jQuery plugins
    table.empty();

    htmlHead = '<tr>' +
        '<th>ID</th>'+
        '<th>Match tick id</th>' +
        '<th>Match minute</th>' +
        '<th>Last modified</th>' +
        '<th>Journal</th>' +
        '</tr>';
    table.append(htmlHead);
    $.each(ticks_list, function(idx, row) {
        var html = '<tr>' +
            '<td>' + row['tick_id'] + '</td>' +
            '<td>' + row['tick'] + '</td>' +
            '<td>' + row['minute'] + '</td>' +
            '<td>' + row['modified'] + '</td>' +
            '<td>' + 'modified' + '</td>' +
            '</tr>';
        table.append(html);
    });
};

/**
 * Loads the match with a given id and renders it on the interface
 * @param match_id
 * @param canvas
 */
dream.Simulator.load_match = function(match_id, canvas) {
    var params = {
        'match-id': match_id,
        'get-board': true,
        'get-ticks': -1
    };

    $.ajax({
        url: dream.Context['simulator-api'],
        method: 'POST',
        data: params,
        dataType: 'json',
        success: function(data) {
            canvas.load_board($.parseJSON(data['board-state']));
            dream.Simulator.load_ticks(data['ticks-list']);
            dream.Simulator.set_loaded_match_id(match_id);
        },
        beforeSend: dream.utils.setCsrfToken()
    });
};

dream.Simulator.new_tick = function(match_id, canvas) {
        var params = {
        'match-id': match_id,
        'get-board': true,
        'get-ticks': -1,
        'new-tick': true
    };

    $.ajax({
        url: dream.Context['simulator-api'],
        method: 'POST',
        data: params,
        dataType: 'json',
        success: function(data) {
            canvas.load_board($.parseJSON(data['board-state']));
            dream.Simulator.load_ticks(data['ticks-list']);
        },
        beforeSend: dream.utils.setCsrfToken()
    });
};

/**
 * The currently loaded match id
 * @returns {*}
 */
dream.Simulator.get_loaded_match_id = function() {
    var match_id = parseInt( $('#field-canvas-match-id').val() );

    if ( !isNaN(match_id) ) {
        return match_id;
    }

    return false;
};

/**
 * Sets the currently loaded match id (on successful server response)
 * @param match_id
 */
dream.Simulator.set_loaded_match_id = function(match_id) {
    $('#field-canvas-match-id').val(match_id);
};

// ############################################################################
// ############################################################################
dream.Simulator.actions = {};

/**
 * Handles the 'load match' button after the selection was done
 * @param event
 */
dream.Simulator.actions.select_match = function(event) {
    var match_id, selected_option, canvas;

    canvas = event.data['canvas'];

    selected_option = $('#select-match').find(':selected');
    match_id = parseInt( selected_option.val() );

    if ( !isNaN(match_id) ) {
        dream.Simulator.load_match(match_id, canvas);
    }
};

/**
 * Handles the 'new tick' button
 * @param event
 */
dream.Simulator.actions.sim_new_tick = function(event) {
    var canvas = event.data['canvas'],
        match_id = dream.Simulator.get_loaded_match_id();

    if (false === match_id) {
        //No match selected
        alert('No match selected');
    }

    console.log('Create new tick for match_id: ' + match_id);
    dream.Simulator.new_tick(match_id, canvas);
};

// ############################################################################
// ############################################################################
$(document).ready(function() {
    var canvas, context;

    context = {};

    canvas = new dream.Canvas('field-canvas');
    canvas.initialize();

    context['canvas'] = canvas;

    $('#btn-match-selected').click(context, dream.Simulator.actions.select_match);
    $('#btn-sim-new-tick').click(context, dream.Simulator.actions.sim_new_tick);

    // TODO: [01.01.2016] > Previous/Next and delete tick buttons
});
