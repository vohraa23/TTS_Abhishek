document.addEventListener('DOMContentLoaded', function() {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('Connected to server');
    });

    socket.on('update_status', function(data) {
        const statusDiv = document.getElementById('status');
        statusDiv.innerHTML = `Progress: ${data.percentage.toFixed(2)}% | ETA: ${data.eta} seconds`;
    });

    socket.on('task_completed', function() {
        const statusDiv = document.getElementById('status');
        statusDiv.innerHTML = 'Task Completed!';
    });

    const form = document.getElementById('textForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const text = document.getElementById('text').value;
        console.log('Text to be converted:', text);  // Add this line
        socket.emit('generate_audio', { text: text });
    });
});