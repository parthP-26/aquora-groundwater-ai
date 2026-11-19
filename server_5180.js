const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 5180;
const filePath = path.join(__dirname, 'groundwater_ai_portal.html');

http.createServer((req, res) => {
  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(500);
      res.end('Error loading portal: ' + err.message);
      return;
    }
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(content);
  });
}).listen(PORT, '0.0.0.0', () => {
  console.log(`AquaAI Portal running at http://localhost:${PORT}/`);
});
