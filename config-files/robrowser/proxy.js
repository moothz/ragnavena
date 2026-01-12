const WebSocket = require('ws');
const net = require('net');
const url = require('url');

const wss = new WebSocket.Server({ port: 25999 });

wss.on('connection', function connection(ws, req) {
  console.log(`[DEBUG] Incoming Request URL: ${req.url}`);
  const parameters = url.parse(req.url, true);
  let targetPort = 26900; // Default to Login Server
  let targetHost = '127.0.0.1';

  // Parse port from query string ?port=XXXX
  if (parameters.query.port) {
    targetPort = parseInt(parameters.query.port);
  } 
  // Parse from path /IP:PORT (roBrowser legacy format)
  else if (req.url) {
      // Remove leading slash
      const path = req.url.substring(1);
      const parts = path.split(':');
      if (parts.length === 2) {
          // targetHost = parts[0]; // We force 127.0.0.1 for security/tunneling
          targetPort = parseInt(parts[1]);
      }
  }

  const allowedPorts = [26900, 26121, 25121];
  if (!allowedPorts.includes(targetPort)) {
      console.log('Blocked connection to port ' + targetPort);
      ws.close();
      return;
  }

  console.log(`[${new Date().toISOString()}] New connection, forwarding to ${targetHost}:${targetPort}`);

  const client = new net.Socket();
  let messageBuffer = [];
  let isTcpConnected = false;

  client.connect(targetPort, targetHost, function() {
    console.log(`[${new Date().toISOString()}] Connected to game server at ${targetPort}`);
    isTcpConnected = true;
    flushBuffer();
  });

  function flushBuffer() {
    if (messageBuffer.length > 0) {
        console.log(`[${new Date().toISOString()}] Flushing ${messageBuffer.length} buffered messages to TCP`);
        for (const msg of messageBuffer) {
            if (msg.length >= 2) {
                const packetId = msg.readUInt16LE(0);
                console.log(`[DEBUG] Client sent Packet ID: 0x${packetId.toString(16)} (Len: ${msg.length})`);
            }
            client.write(msg);
        }
        messageBuffer = [];
    }
  }

  ws.on('message', function incoming(message) {
    if (isTcpConnected) {
      const len = Buffer.isBuffer(message) ? message.length : message.length;
      console.log(`[${new Date().toISOString()}] WS -> TCP: ${len} bytes`);
      if (Buffer.isBuffer(message) && message.length >= 2) {
          const packetId = message.readUInt16LE(0);
          console.log(`[DEBUG] Client sent Packet ID: 0x${packetId.toString(16)}`);
      }
      client.write(message);
    } else {
        const len = Buffer.isBuffer(message) ? message.length : message.length;
        console.log(`[${new Date().toISOString()}] WS -> TCP: Buffered ${len} bytes (TCP connecting)`);
        messageBuffer.push(message);
    }
  });

  client.on('data', function(data) {
    if (ws.readyState === ws.OPEN) {
      console.log(`[${new Date().toISOString()}] TCP -> WS: ${data.length} bytes`);
      if (data.length >= 2) {
          const packetId = data.readUInt16LE(0);
          console.log(`[DEBUG] Server replied Packet ID: 0x${packetId.toString(16)}`);
          if (packetId === 0x6a && data.length >= 3) {
              const errorCode = data.readUInt8(2);
              console.log(`[DEBUG] Login Error Code: ${errorCode}`);
          }
      }
      ws.send(data);
    }
  });

  ws.on('close', function() {
    console.log(`[${new Date().toISOString()}] WS Closed`);
    client.end();
  });

  client.on('close', function() {
    console.log(`[${new Date().toISOString()}] TCP Closed`);
    ws.close();
  });

  client.on('error', function(err) {
    console.error(`[${new Date().toISOString()}] TCP error on port ${targetPort}:`, err.message);
    ws.close();
  });
});

console.log('WebSocket Proxy listening on port 25999');