//SETUP
//enable websocket
var socket = io();

//lidar graph widget setup
var lidarGraph = document.getElementById('lidarGraph');
var ctx = lidarGraph.getContext("2d");
var pixelSize = 1;

//livestream widget setup
var livestream = document.getElementById('livestream')

//speed widget setup
var speedSlider = document.getElementById("speedSlider");
var speedSpan = document.getElementById("speedSpan");
speedSpan.innerHTML = speedSlider.value;

//pixel size input setup
var pixelSizeInput = document.getElementById("pixelSizeInput");


//LISTENERS
socket.on('connect', function(){
    console.log('connected');
    //comment out what is not needed
    //socket.emit('needCamera');
    socket.emit('needLidar');
});

socket.on('disconnect', function(){
    console.log('disconnected');
});

socket.on('jpg_string', function(data){
    livestream.src = 'data:image/jpeg;base64,' + data;
})

socket.on('scanData', function(data) {
    //clear the old canvas
    ctx.clearRect(0, 0, lidarGraph.width, lidarGraph.height);

    //draw the robot shape
    ctx.strokeStyle = "#0000FF";
    ctx.strokeRect(
        (SCREEN_WIDTH / 2) - (ROBOT_WIDTH * PIXEL_PER_CM / 2), 
        (SCREEN_WIDTH / 2) - (ROBOT_LENGTH * PIXEL_PER_CM / 2), 
        ROBOT_WIDTH * PIXEL_PER_CM, 
        ROBOT_LENGTH * PIXEL_PER_CM);

    //Plot every array point
    for (let i=0;i<360;i++) {
        //lidar is turned 90 degrees too much to the right
        radians = (i + 90) * (Math.PI / 180);
        distance = data[i];
        x = distance * Math.cos(radians);
        y = distance * Math.sin(radians);
        scaled_x = (SCREEN_WIDTH / 2) + (x * PIXEL_PER_CM);
        scaled_y = (SCREEN_WIDTH / 2) + (y * PIXEL_PER_CM);

        //This tells us where angle 180 on the lidar is
        if (i == 180) {
            //draw special point
            ctx.fillStyle = "#FF0000";
            ctx.fillRect(
                scaled_x - pixelSize, 
                scaled_y - pixelSize, 
                pixelSize * 2, 
                pixelSize * 2);
        }
        else {
            //draw regular point
            ctx.fillStyle = "#000000";
            ctx.fillRect(
                scaled_x - (pixelSize / 2), 
                scaled_y - (pixelSize / 2), 
                pixelSize, 
                pixelSize);
        }
    }
});


//SENDERS
//button presses
function motorsOn(){
    socket.emit('motorsOn');
}

function motorsOff(){
    socket.emit('motorsOff');
}

function turnLeft(){
    socket.emit('turnLeft');
}

function turnRight(){
    socket.emit('turnRight');
}

function forward(){
    socket.emit('forward');
}

function backward(){
    socket.emit('backward');
}

function stopMotors(){
    socket.emit('stopMotors')
}

//speed slider
speedSlider.oninput = function() {
    speedSpan.innerHTML = this.value;
    socket.emit('setSpeed', this.value)
}

//pixel size input
pixelSizeInput.oninput = function() {
    pixelSize = parseInt(this.value);
}