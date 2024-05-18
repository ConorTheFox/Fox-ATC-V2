var messageCount = 0;

function monitor() {
    const centerBox = document.getElementById('center-box');

    centerBox.innerHTML = `
        <div id="message-box">
            <p>Monitoring communications for SAN...</p>
        </div>
    `;

    centerBox.style.height = '700px';
    centerBox.style.width = '350px';
    centerBox.style.padding = '20px';

    const messageBox = document.getElementById('message-box');
    messageBox.style.display = 'block';

    const ws = new WebSocket('ws://localhost:3000');

    ws.onopen = () => {
        console.log('Connected to Server!');
        ws.send('Monitoring Communications...');
    };

    ws.onmessage = (message) => {
        console.log('Message Received: ', message.data);
        if(messageCount === 0) {
            messageBox.innerHTML = `<div class="message"><p>${message.data}</p></div>`;
            messageCount++;
        } else {
            messageBox.innerHTML += `<div class="message"><p>${message.data}</p></div>`;   
        }
    };

    ws.onclose = () => {
        console.log('Disconnected from Server!');
        ws.close();
    };
}