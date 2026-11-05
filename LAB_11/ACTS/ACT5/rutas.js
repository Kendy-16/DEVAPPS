/// ARCHIVO ESPECIALIZADO DE MANEJO DE RUTAS

// creando gestionador de rutas
var express = require('express');
var router = express.Router();

// Creando manejadores de rutas
router.get('/', function(req, res){
    res.send('Pagina principal');
});

router.get('/login', function(req, res){
    res.send('Inicia sesion');
});

router.get('/productos', function(req, res){
    res.send('catalogo de productos');
});

router.get('/productos/compra', function(req, res){
    res.send('Aqui puedes comprar tus productos');
});

module.exports = router;