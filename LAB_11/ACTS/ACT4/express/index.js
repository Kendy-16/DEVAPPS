 // importando paquete Express
var express = require('express');

// creando aplicación en Express
var app = express();

// Creando manejadores de rutas
app.get('/',function(req,res){
    res.send('Hola mundo desde Express');
});

app.get('/login',function(req,res){
    res.send('Aquí se mostraría la pagina del login');
});

// El servidor de escucha que desplegará mi ruta HTTP
app.listen(3000,function(){
    console.log('La aplicación está funcionando en el puerto 3000');
});