import assert from "node:assert/strict";
import { legacy_createStore as createStore } from "redux";
import gastosReducer from "../src/store/gastosReducer.js";
import {
  agregarGasto,
  eliminarGasto,
} from "../src/store/acciones.js";

const store = createStore(gastosReducer);

const gasto1 = {
  id: "g1",
  descripcion: "Almuerzo",
  monto: 32.5,
  categoria: "Alimentación",
  fecha: "2026-10-02T12:00:00.000Z",
};

const gasto2 = {
  id: "g2",
  descripcion: "Pasaje",
  monto: 18,
  categoria: "Transporte",
  fecha: "2026-10-02T12:00:00.000Z",
};

const gasto3 = {
  id: "g3",
  descripcion: "Material de estudio",
  monto: 54,
  categoria: "Estudios",
  fecha: "2026-10-02T12:00:00.000Z",
};

const estadoAnterior = store.getState();

store.dispatch(agregarGasto(gasto1));
store.dispatch(agregarGasto(gasto2));
store.dispatch(agregarGasto(gasto3));

console.log("Después de agregar:", store.getState().gastos);

assert.equal(store.getState().gastos.length, 3);
assert.deepEqual(estadoAnterior.gastos, []);

store.dispatch(eliminarGasto("g2"));

const gastosFinales = store.getState().gastos;
const totalFinal = gastosFinales.reduce(
  (suma, gasto) => suma + gasto.monto,
  0
);

console.log("Después de eliminar:", gastosFinales);
console.log("Total final: S/", totalFinal);

assert.equal(gastosFinales.length, 2);
assert.equal(totalFinal, 86.5);

console.log("Prueba manual completada correctamente.");