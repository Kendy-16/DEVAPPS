let pagina = 1;
let limite = 10;
let filtro = "";

// Evita mostrar respuestas antiguas si el usuario e inicia varias búsquedas rápidamente.
let controladorActual = null;

const tabla = document.getElementById("tablaInventario");
const formulario = document.getElementById("formBusqueda");
const btnAnterior = document.getElementById("btnAnterior");
const btnSiguiente = document.getElementById("btnSiguiente");
const btnLimpiar = document.getElementById("btnLimpiar");
const mensaje = document.getElementById("mensaje");
const estadoServidor = document.getElementById("estadoServidor");

// ----------------------------------------------------------
// 1. CONSULTA HTTP
// ----------------------------------------------------------

async function cargarInventario() {

    if (controladorActual) {
        controladorActual.abort();
    }

    controladorActual = new AbortController();

    const parametros = new URLSearchParams({
        pagina: String(pagina),
        limite: String(limite),
        filtro: filtro
    });

    const url = `/api/inventario?${parametros.toString()}`;

    mostrarMensaje("Consultando inventario...", "info");

    try {
        const respuesta = await fetch(url, {
            signal: controladorActual.signal
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(
                resultado.detalle ||
                resultado.mensaje ||
                "Error desconocido."
            );
        }

        renderizarTabla(resultado.datos);
        actualizarPaginacion(resultado.metadatos);

        estadoServidor.textContent = "Servidor conectado";
        estadoServidor.classList.remove("desconectado");

        ocultarMensaje();

        if (resultado.datos.length === 0) {
            mostrarMensaje(
                "No se encontraron productos para esta consulta.",
                "info"
            );
        }

    } catch (error) {

        if (error.name === "AbortError") {
            return;
        }

        tabla.replaceChildren();

        estadoServidor.textContent = "Error de conexión";
        estadoServidor.classList.add("desconectado");

        mostrarMensaje(error.message, "error");

    }
}

// ----------------------------------------------------------
// 2. PRESENTACIÓN DE PRODUCTOS
// ----------------------------------------------------------

function renderizarTabla(articulos) {

    tabla.replaceChildren();

    const formatoPrecio = new Intl.NumberFormat("es-PE", {
        style: "currency",
        currency: "PEN"
    });

    for (const articulo of articulos) {

        const fila = document.createElement("tr");

        // Se usa textContent, evitando insertar HTML
        // procedente de datos externos.
        const id = document.createElement("td");
        id.textContent = articulo.id;

        const nombre = document.createElement("td");
        nombre.className = "producto-nombre";
        nombre.textContent = articulo.nombre;

        const celdaCategoria = document.createElement("td");
        const categoria = document.createElement("span");

        categoria.className = "categoria";
        categoria.textContent = articulo.categoria;

        celdaCategoria.appendChild(categoria);

        const precio = document.createElement("td");
        precio.textContent = formatoPrecio.format(articulo.precio);

        const celdaStock = document.createElement("td");
        const stock = document.createElement("span");

        stock.className = articulo.stock === 0
            ? "stock agotado"
            : "stock";

        stock.textContent = articulo.stock === 0
            ? "Agotado"
            : `${articulo.stock} unidades`;

        celdaStock.appendChild(stock);

        fila.append(
            id,
            nombre,
            celdaCategoria,
            precio,
            celdaStock
        );

        tabla.appendChild(fila);
    }
}

// ----------------------------------------------------------
// 3. METADATOS DE PAGINACIÓN
// ----------------------------------------------------------

function actualizarPaginacion(meta) {

    document.getElementById("totalRegistros").textContent =
        meta.total_registros;

    document.getElementById("paginaActual").textContent =
        meta.pagina_actual;

    document.getElementById("totalPaginas").textContent =
        meta.total_paginas;

    document.getElementById("numeroPagina").textContent =
        meta.pagina_actual;

    document.getElementById("informacionPagina").textContent =
        `Mostrando ${meta.registros_mostrados} de ` +
        `${meta.total_registros} resultados`;

    btnAnterior.disabled = !meta.hay_pagina_anterior;
    btnSiguiente.disabled = !meta.hay_pagina_siguiente;
}

// ----------------------------------------------------------
// 4. MENSAJES
// ----------------------------------------------------------

function mostrarMensaje(texto, tipo) {
    mensaje.textContent = texto;
    mensaje.className = `mensaje visible ${tipo}`;
}

function ocultarMensaje() {
    mensaje.textContent = "";
    mensaje.className = "mensaje";
}

// ----------------------------------------------------------
// 5. EVENTOS DEL FORMULARIO
// ----------------------------------------------------------

formulario.addEventListener("submit", (evento) => {

    evento.preventDefault();

    filtro = document.getElementById("filtro").value.trim();
    limite = Number(document.getElementById("limite").value);

    pagina = 1;

    cargarInventario();
});

btnAnterior.addEventListener("click", () => {

    if (pagina > 1) {
        pagina--;
        cargarInventario();
    }
});

btnSiguiente.addEventListener("click", () => {

    pagina++;
    cargarInventario();
});

btnLimpiar.addEventListener("click", () => {

    document.getElementById("filtro").value = "";
    document.getElementById("limite").value = "10";

    filtro = "";
    pagina = 1;
    limite = 10;

    cargarInventario();
});

// ----------------------------------------------------------
// 6. INICIALIZACIÓN
// ----------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    cargarInventario();
});
