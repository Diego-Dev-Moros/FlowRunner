// vistas/services/registry.js
import { FUNCTION_CATALOG } from './catalog.js';

let enabledSet = null;

// Llamar una vez al iniciar
export async function bootstrapFlags() {
  try {
    if (window.eel && typeof window.eel.get_enabled_types === 'function') {
      const arr = await window.eel.get_enabled_types()();
      enabledSet = new Set(arr || []);
    }
  } catch (e) {
    enabledSet = null;
  }
}

// Devuelve catálogo filtrado (si no hay flags, devuelve todo)
export function listEnabled() {
  if (!enabledSet || enabledSet.size === 0) return FUNCTION_CATALOG;
  return FUNCTION_CATALOG.filter(def => enabledSet.has(def.id));
}

export function listByCategory() {
  const defs = listEnabled();
  const map = {};
  defs.forEach(def => {
    (map[def.categoria] ||= []).push(def);
  });
  return map;
}

export function getDefById(id) {
  return (FUNCTION_CATALOG.find(d => d.id === id) || null);
}
