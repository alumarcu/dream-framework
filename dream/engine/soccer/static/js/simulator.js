
var drawBoardToCanvas = function(boardData, canvasId, settings) {
    var canvas, canvasContext, gw, glen, maxw, maxlen, lenUnit, wUnit, x, y, i, playerCoords;

    canvas = document.getElementById(canvasId);
    canvasContext = canvas.getContext('2d');

    // grid dimensions
    gw = settings.gridWidth;
    glen = settings.gridLength;

    maxw = canvas.width;
    maxlen = canvas.height;

    canvasContext.strokeStyle = settings.lineColor;

    lenUnit = maxlen / glen;
    wUnit = maxw / gw;

    x = 0; y = 0;

    // draws all horizontal lines on the canvas
    for (i = 0; i < glen; i++) {
        y = i * lenUnit;

        canvasContext.moveTo(x, y);
        canvasContext.lineTo(maxw, y);
        canvasContext.stroke();
    }

    // draws all vertical lines on the canvas
    y = 0;
    for (i = 0; i < gw; i++) {
        x = i * wUnit;

        canvasContext.moveTo(x, y);
        canvasContext.lineTo(x, maxlen);
        canvasContext.stroke();
    }

    // place each player on the canvas
    playerCoords = boardData.player_coordinates;

    $.each(playerCoords, function(idx, coords) {
        var x, y;
        x = coords[0];
        y = coords[1];

        canvasContext.beginPath();
        canvasContext.strokeStyle = settings.playerColor;
        canvasContext.arc(x * wUnit, y * lenUnit, 4, 0, 2 * Math.PI);
        canvasContext.stroke();
    });

}