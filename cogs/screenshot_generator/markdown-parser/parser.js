const { toHTML } = require('discord-markdown');

const PORT = 33334;
const HOST = 'localhost';
const dgram = require('dgram');
const server = dgram.createSocket('udp4');


server.on('message', function (message, remote) {
  server.send(toHTML(message.toString()), remote.port);
});
server.bind(PORT, HOST);
