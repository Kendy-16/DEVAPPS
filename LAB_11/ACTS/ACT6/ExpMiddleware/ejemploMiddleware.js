// importando paquete express
var express = require('express');

// creando objeto express
var app = express();

// creando el middleware
const middleware = function(req, res, next){
    console.log('ejecutando el middleware mientras llega petición');
    next();
};

// invocando el middleware
app.use(middleware);

// configurando manejador de rutas
app.get('/', function(req, res){
    res.send('Llegó petición al servidor');
});

// levantando servidor
app.listen(3000, function(){
    console.log('servidor en escucha');
});