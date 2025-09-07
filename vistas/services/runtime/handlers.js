// Handlers de ejecución por id. Si no hay handler, intenta Eel; si no, stub OK.
const HANDLERS = {
  abrir_pagina: async ({ url }) => { window.open(url, '_blank'); return { ok:true, opened:url }; },
  escribir_txt: async ({ variable, ruta, delimitador }) => {
    // ejemplo stub: simula escribir
    await sleep(300);
    return { ok:true, saved:ruta, rows: Array.isArray(variable) ? variable.length : 1 };
  },
  ejecutar_flujo: async () => ({ ok:true })
};

export async function runFunction(defId, props) {
  if (HANDLERS[defId]) return HANDLERS[defId](props || {});
  if (window.eel?.run_step) {
    // llama a Python (Eel) si existe
    const res = await window.eel.run_step(defId, props || {})(); // devuelve Promesa
    return res;
  }
  // stub por defecto
  await sleep(200);
  return { ok:true, message:`(stub) ${defId} ejecutado` };
}

function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }

export function formatRunnerError(error) {
  if (typeof error === 'string') {
    return error;
  }
  if (error && error.message) {
    return error.message;
  }
  if (error && error.error) {
    return error.error;
  }
  return 'Error desconocido en la ejecución';
}
