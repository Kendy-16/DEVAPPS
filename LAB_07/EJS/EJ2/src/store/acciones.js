export const AGREGAR_GASTO = "AGREGAR_GASTO";
export const ELIMINAR_GASTO = "ELIMINAR_GASTO";

export function agregarGasto(gasto) {
  return {
    type: AGREGAR_GASTO,
    payload: gasto,
  };
}

export function eliminarGasto(id) {
  return {
    type: ELIMINAR_GASTO,
    payload: id,
  };
}