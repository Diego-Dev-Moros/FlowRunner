export const state = {
  steps: [],
  edges: [],
  seq: 1,
  selectedStepId: null,
  lastStepId: null,

  addStep(def, pos) {
    const id = `step_${this.seq++}`;
    const step = {
      id,
      defId: def.id,
      label: def.nombre,
      categoria: def.categoria,
      pos: { x: pos.x, y: pos.y },
      props: {},
      ports: { in: ['W','N'], out: ['E','S'] },
    };
    this.steps.push(step);
    return step;
  },

  getStep(id){ return this.steps.find(s => s.id === id); },

  /** Reconecta predecesores → sucesores al eliminar un nodo */
  removeStep(stepId) {
    // 1) obtener preds/succs
    const preds = this.edges.filter(e => e.to.step   === stepId).map(e => e.from.step);
    const succs = this.edges.filter(e => e.from.step === stepId).map(e => e.to.step);

    // 2) remover edges tocando el nodo
    this.edges = this.edges.filter(e => e.from.step !== stepId && e.to.step !== stepId);

    // 3) quitar el nodo
    this.steps = this.steps.filter(s => s.id !== stepId);

    // 4) reencableado si corresponde (emparejo por Y)
    if (preds.length && succs.length) {
      const byY = id => (this.getStep(id)?.pos?.y ?? 0);
      preds.sort((a,b) => byY(a) - byY(b));
      succs.sort((a,b) => byY(a) - byY(b));
      const n = Math.min(preds.length, succs.length);

      for (let i = 0; i < n; i++) {
        const from = preds[i], to = succs[i];
        if (!from || !to || from === to) continue;
        // evitar duplicados exactos
        const dup = this.edges.some(e => e.from.step === from && e.to.step === to);
        if (!dup) {
          this.edges.push({
            id: `edge_${Date.now()}_${Math.random().toString(36).slice(2,7)}`,
            from: { step: from, port: 'E' },
            to:   { step: to,   port: 'W' }
          });
        }
      }
    }

    if (this.selectedStepId === stepId) this.selectedStepId = null;
    if (this.lastStepId === stepId) this.lastStepId = null;
  },

  addEdge(from, to) {
    // evita duplicados/self-loop
    if (!from || !to || from.step === to.step) return null;
    const dup = this.edges.some(e => e.from.step === from.step && e.to.step === to.step);
    if (dup) return null;
    const edge = {
      id: `edge_${Date.now()}_${Math.random().toString(36).slice(2,7)}`,
      from, to
    };
    this.edges.push(edge);
    return edge;
  },

  setSelected(id){ this.selectedStepId = id; }
};
