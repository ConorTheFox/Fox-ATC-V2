// --- Initial Setup --- //

// Log Version
const VERSION = "2.0.0";
console.log(`Server Version: ${VERSION}`);

// Import Required Modules
const express = require("express");
const cors = require("cors"); // For Local Development
const ws = require("ws");
const http = require("http");

// Express App Setup
const app = express();
app.use(cors()); // For Local Development
app.use(express.text()); // Use text middleware for plain text messages

// HTTP Server Setup
const server = http.createServer(app);
const PORT = 3000;

// WebSocket Server Setup
const wss = new ws.Server({ server });

// --- Express Server --- //

// Receive Message From Python
app.post("/message", (req, res) => {
    const message = req.body; // Plain text message
    // Log Message
    console.log("Message Received: ", message);

    // Send Message To All Clients
    wss.clients.forEach((client) => {
        if (client.readyState === ws.OPEN) {
            client.send(message);
        }
    });

    // Send Response
    res.send("Message Received!");
});

// Set Server To Listen
server.listen(PORT, () => {
    console.log(`Server Listening on Port ${PORT}`);
});

// --- WebSocket Server --- //

// Websocket Connection
wss.on("connection", (ws) => {
    // Log Connection
    console.log("Client Connected!");
});

// WebSocket Server Close
wss.on("close", () => {
    // Log Connection
    console.log("Client Disconnected!");
});
