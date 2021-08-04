//SETUP
const socket = io();
const livestream = document.getElementById('livestream')

//LISTENERS
socket.on('connect', function(){
    console.log('connected');
    socket.emit('recordingSystem');
});
socket.on('disconnect', function(){
    console.log('disconnected');
});
socket.on('jpg_string', function(data){
    livestream.src = 'data:image/jpeg;base64,' + data;
})

//SENDERS
function startRecording() {
    motorBias = 0;
    socket.emit('startRecording');
    console.log('starting the recording');
}
function pauseRecording() {
    socket.emit('pauseRecording');
    console.log('pausing the recording');
}
function motorsOn(){
    socket.emit('motorsOn');
}
function motorsOff(){
    socket.emit('motorsOff');
}
var motorBias = 0;
var biasDisplay = document.getElementById("biasDisplay");
function turnLeft(){
    motorBias -= 2;
    socket.emit('motorBias', motorBias);
    biasDisplay.innerHTML = motorBias;
}
function turnRight(){
    motorBias += 2;
    socket.emit('motorBias', motorBias);
    biasDisplay.innerHTML = motorBias;
}