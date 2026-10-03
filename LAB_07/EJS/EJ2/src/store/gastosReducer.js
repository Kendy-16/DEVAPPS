import {
  AGREGAR_GASTO,
  ELIMINAR_GASTO,
} from "./acciones.js";

const estadoInicial = {
  gastos: [],
};

export default function gastosReducer(
  estado = estadoInicial,
  accion
) {
  switch (accion.type) {
    case AGREGAR_GASTO:
      return {
        ...estado,
        gastos: [...estado.gastos, accion.payload],
      };

    case ELIMINAR_GASTO:
      return {
        ...estado,
        gastos: estado.gastos.filter(
          (gasto) => gasto.id !== accion.payload
        ),
      };

    default:
      return estado;
  }
}