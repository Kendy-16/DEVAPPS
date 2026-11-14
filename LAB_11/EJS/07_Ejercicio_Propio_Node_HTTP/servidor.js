// Ejercicio propio Node 01: servidor nativo con rutas y parámetros query.
const http=require('node:http');
const fs=require('node:fs/promises');
const path=require('node:path');
const {URL}=require('node:url');
const PORT=Number(process.env.PORT||4201);
let visitas=0;
const archivos={'/':'index.html','/style.css':'style.css','/app.js':'app.js'};
const tipos={'index.html':'text/html; charset=utf-8','style.css':'text/css; charset=utf-8','app.js':'text/javascript; charset=utf-8'};
http.createServer(async(req,res)=>{
 const u=new URL(req.url,'http://localhost');
 if(req.method!=='GET'){res.writeHead(405);return res.end('Método no permitido');}
 if(u.pathname==='/api/estacion'){res.writeHead(200,{'Content-Type':'application/json; charset=utf-8'});return res.end(JSON.stringify({visitas,servidor:'Node HTTP',actualizado:new Date().toISOString()}));}
 if(u.pathname==='/api/saludo'){
   const nombre=(u.searchParams.get('nombre')||'Visitante').trim().slice(0,50);
   res.writeHead(200,{'Content-Type':'application/json; charset=utf-8'});
   return res.end(JSON.stringify({mensaje:`Hola, ${nombre||'Visitante'}. Respuesta generada por Node.js.`}));
 }
 const archivo=archivos[u.pathname];if(!archivo){res.writeHead(404);return res.end('Ruta no encontrada');}
 try{const contenido=await fs.readFile(path.join(__dirname,'public',archivo));if(u.pathname==='/')visitas++;
 res.writeHead(200,{'Content-Type':tipos[archivo], 'X-Content-Type-Options':'nosniff'});res.end(contenido);
 }catch(error){console.error(error);res.writeHead(500);res.end('Error al abrir el archivo');}
}).listen(PORT,()=>console.log(`RADAR HTTP: http://localhost:${PORT}`));
