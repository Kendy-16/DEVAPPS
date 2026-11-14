const http = require('node:http');
const fs = require('node:fs/promises');
const path = require('node:path');
const { URL } = require('node:url');
const PUBLIC = path.join(__dirname, 'public');
const FILES = { '/': ['index.html', 'text/html; charset=utf-8'], '/style.css': ['style.css','text/css; charset=utf-8'], '/app.js': ['app.js', 'text/javascript; charset=utf-8'] };
const PORT = Number(process.env.PORT || 4203);
http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const file = FILES[url.pathname];
  if (!file || req.method !== 'GET') { res.writeHead(404, {'Content-Type':'text/plain; charset=utf-8'}); return res.end('404 · Recurso no encontrado'); }
  try {
    const data = await fs.readFile(path.join(PUBLIC,file[0]));
    res.writeHead(200, {'Content-Type':file[1], 'X-Content-Type-Options':'nosniff'});
    res.end(data);
  } catch (error) { console.error(error); res.writeHead(500); res.end('Error del servidor'); }
}).listen(PORT, () => console.log(`Servidor Node disponible en http://localhost:${PORT}`));
