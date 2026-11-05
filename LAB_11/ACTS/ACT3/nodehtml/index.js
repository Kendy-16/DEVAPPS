// importar paquetes http y fs
var http = require('http'),
    fs = require('fs');

// creación de plantilla
var html = fs.readFileSync("./index.html");

// crear servidor, ponerlo a la escucha y desplegar contenido de plantilla
http.createServer(function(req,res){
    res.write(html);
    res.end();
}).listen(3000);