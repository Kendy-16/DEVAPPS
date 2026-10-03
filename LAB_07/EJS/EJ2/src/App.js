import FormularioGasto from "./components/FormularioGasto";
import ListaGastos from "./components/ListaGastos";
import ResumenGastos from "./components/ResumenGastos";
import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="encabezado">
        <span className="etiqueta">CONTROL PERSONAL</span>
        <h1>Mis gastos</h1>
        <p>Registra tus movimientos y conoce cuánto has gastado.</p>
      </header>

      <main className="contenido">
        <section className="panel-formulario">
          <h2>Nuevo gasto</h2>
          <FormularioGasto />
        </section>

        <section className="panel-resumen">
          <ResumenGastos />
        </section>

        <section className="panel-lista">
          <h2>Historial de gastos</h2>
          <ListaGastos />
        </section>
      </main>
    </div>
  );
}

export default App;