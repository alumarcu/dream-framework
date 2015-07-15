"use strict";

var dream = dream || {};

dream.Canvas = function(elementId) {
    // Perform GET call to fetch board settings
    this.canvas = document.getElementById(elementId); // TODO: Throw error if nothing is found
    this.context = this.canvas.getContext('2d');
};

// TODO: can you make it work without having these as static props ??
dream.Canvas.settings = {};
dream.Canvas.initd = false;

dream.Canvas.prototype.initialize = function() {
    var location, params;

    location = window.location.href;
    params = {setup: 1};

        $.ajax({
            url: location + '?' + $.param(params),
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                // do stuff with the data
                dream.Canvas.settings = data.setup;
                // TODO -> unlock screen for extra actions
                dream.Canvas.initd = true;
                console.log("OK - canvas initialized");
            }
        });
};

dream.Canvas.prototype.load_board = function(data) {
    console.log("Loading Board");
    console.log(dream.Canvas.initd);
    if (dream.Canvas.initd) {
        var board_state;
        board_state = $.parseJSON(data['board_state']);
        this.draw_board(board_state);
    }
};

dream.Canvas.prototype.draw_board = function(board_data) {
    var grid_width, grid_length,
        canvas_width, canvas_length,
        unit_of_width, unit_of_length,
        x, y, i, player_coordinates;

    grid_width = dream.Canvas.settings['grid_width'];
    grid_length = dream.Canvas.settings['grid_length'];

    canvas_width = this.canvas.width;
    canvas_length = this.canvas.height;

    this.context.strokeStyle = '#4DB779';

    unit_of_width = canvas_length / grid_length;
    unit_of_length = canvas_width / grid_width;

    x = 0; y = 0;

    // draws all horizontal lines on the canvas
    for (i = 0; i < grid_length; i++) {
        y = i * unit_of_width;

        this.context.moveTo(x, y);
        this.context.lineTo(canvas_width, y);
        this.context.stroke();
    }

    // draws all vertical lines on the canvas
    y = 0;
    for (i = 0; i < grid_width; i++) {
        x = i * unit_of_length;

        this.context.moveTo(x, y);
        this.context.lineTo(x, canvas_length);
        this.context.stroke();
    }

    player_coordinates = board_data['player_coordinates'];

    for (i = 0; i < player_coordinates.length; i++) {
        var coords = player_coordinates[i];
        x = coords[0];
        y = coords[1];

        this.context.beginPath();
        this.context.strokeStyle = '#000000';
        this.context.arc(x * unit_of_length, y * unit_of_width, 4, 0, 2 * Math.PI);
        this.context.stroke();
    }

};

dream.Simulator = {
    get_ticks_for_match: function(match_id) {
        var location, params;

        location = window.location.href;
        params = {id: match_id, ticks: 1};

        $.ajax({
            url: location + '?' + $.param(params),
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                // do stuff with the data
                if (typeof(response['data']) == 'object' && $.isArray(response['data'])) {
                    var htmlHead, table = $('#ticks');
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
                    $.each(response['data'], function(idx, row) {
                        var html = '<tr>' +
                            '<td>' + row['tick_id'] + '</td>' +
                            '<td>' + row['sim_last_tick_id'] + '</td>' +
                            '<td>' + row['sim_minutes_passed'] + '</td>' +
                            '<td>' + row['last_modified'] + '</td>' +
                            '<td>' + row['journal'] + '</td>' +
                            '</tr>';
                        table.append(html);
                    })
                }
            }
        });
    },

    get_board_for_match: function(match_id, canvas) {
        var location, params;

        location = window.location.href;
        params = {id: match_id, board: 1};

        $.ajax({
            url: location + '?' + $.param(params),
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                // do stuff with the data
                canvas.load_board(data);
            }
        });
    },

    create_next_tick: function(match_id, canvas) {
        var location, params;

        location = window.location.href;
        params = {id: match_id, next_tick: 1};

        $.ajax({
            url: location + '?' + $.param(params),
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                // do stuff with the data
                canvas.load_board(data);
            }
        });
    }
};

$(document).ready(function() {
    var canvas;

    canvas = new dream.Canvas('soccer_field');
    canvas.initialize();

    $('#get_ticks').click(function() {
        var match_id;

        match_id = parseInt( $('#match_id').val() );

        if ( !isNaN( match_id ) ) {
            dream.Simulator.get_ticks_for_match(match_id);
        }
    });

    $('#get_board').click(function() {
        var match_id;

        match_id = parseInt( $('#match_id').val() );

        if ( !isNaN( match_id ) ) {
            dream.Simulator.get_board_for_match(match_id, canvas);
        }
    });

    $('#next_tick').click(function() {
        var match_id;

        match_id = parseInt( $('#match_id').val() );

        if ( !isNaN( match_id ) ) {
            dream.Simulator.create_next_tick(match_id, canvas);
        }
    });

});
