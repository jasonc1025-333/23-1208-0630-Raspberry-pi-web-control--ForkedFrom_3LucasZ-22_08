var socket = io();

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

var slider = document.getElementById("myRange");
var output = document.getElementById("demo");

output.innerHTML = slider.value
slider.oninput = function() {
    output.innerHTML = this.value;
    socket.emit('setSpeed', this.value)
}