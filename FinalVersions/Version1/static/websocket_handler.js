//SETUP
//websocket
var socket = io();
//livestream
var livestream = document.getElementById('livestream')
//speed
var speedSlider = document.getElementById("speedSlider");
var speedSpan = document.getElementById("speedSpan");
speedSpan.innerHTML = speedSlider.value

//LISTENERS
socket.on('connect', function(){
    console.log('connected');
    socket.emit('needCamera')
});
socket.on('disconnect', function(){
    console.log('disconnected');
});
socket.on('jpg_string', function(data){
    livestream.src = 'data:image/jpeg;base64,' + data;
})

//SENDERS
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
//SPEED BAR
speedSlider.oninput = function() {
    speedSpan.innerHTML = this.value;
    socket.emit('setSpeed', this.value)
}