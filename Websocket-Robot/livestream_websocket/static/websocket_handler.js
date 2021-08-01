const socket = io();
const livestream = document.getElementById('livestream')

//LISTENERS
socket.on('jpg_string', function(data){
    livestream.src = 'data:image/jpeg;base64,' + data;
})
socket.on('connect', function(){
    console.log('connected');
    //ask for camera data stream
    socket.emit('server')
});
socket.on('disconnect', function(){
    console.log('disconnected');
});