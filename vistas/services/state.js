// vistas/services/state.js
export const state = {
  steps: [],          // [{ id, defId, label, categoria, pos:{x,y}, props:{}, ports:{in,out} }]
  edges: [],          // [{ id, from:{step,port}, to:{step,port} }]
  seq: 1,
  selectedStepId: null,
  lastStepId: null,
  results: {},        // { stepId: { status, message, preview } }

  // --- CRUD de pasos ---
  addStep(def, pos) {
    const id = `step_${this.seq++}`;
    const step = {
      id,
      defId: def.id,
      label: def.nombre,
      categoria: def.categoria,
      pos: { x: pos.x, y: pos.y },
      props: {},
      ports: { in: ['W','N'], out: ['E','S'] }, // anclajes cardinales
    };
    this.steps.push(step);
    this.lastStepId = id;
    return step;
  },

  getStep(id) { return this.steps.find(s => s.id === id); },

  updateStep(id, patch) {
    const s = this.getStep(id);
    if (!s) return;
    Object.assign(s, patch);
    return s;
  },

  // --- Edges ---
  addEdge(from, to) {
    if (!from || !to || from.step === to.step) return null;
    const dup = this.edges.some(e => e.from.step === from.step && e.to.step === to.step);
    if (dup) return null;
    const edge = { id:`edge_${Date.now()}_${Math.random().toString(36).slice(2,7)}`, from, to };
    this.edges.push(edge);
    return edge;
  },

  // Reconexión inteligente al borrar
  removeStep(stepId) {
    // predecesores y sucesores
    const preds = this.edges.filter(e => e.to.step === stepId).map(e => e.from.step);
    const succs = this.edges.filter(e => e.from.step === stepId).map(e => e.to.step);

    // quitar edges tocando el nodo
    this.edges = this.edges.filter(e => e.from.step !== stepId && e.to.step !== stepId);
    // quitar step
    this.steps = this.steps.filter(s => s.id !== stepId);
    delete this.results[stepId];

    // reconectar por orden Y (si tiene sentido)
    if (preds.length && succs.length) {
      const byY = id => (this.getStep(id)?.pos?.y ?? 0);
      preds.sort((a,b)=>byY(a)-byY(b));
      succs.sort((a,b)=>byY(a)-byY(b));
      const n = Math.min(preds.length, succs.length);
      for (let i=0;i<n;i++){
        if (preds[i] !== succs[i]) {
          this.edges.push({
            id: `edge_${Date.now()}_${i}`,
            from: { step: preds[i], port: 'E' },
            to:   { step: succs[i], port: 'W' }
          });
        }
      }
    }

    if (this.selectedStepId === stepId) this.selectedStepId = null;
    if (this.lastStepId === stepId) this.lastStepId = null;
  },

  removeEdge(edgeId) {
    this.edges = this.edges.filter(e => e.id !== edgeId);
  },

  // --- selección ---
  setSelected(id) { this.selectedStepId = id; },

  // --- resultados por paso (para panel derecho) ---
  setResult(stepId, payload) {
    // payload: { status, message, preview }
    this.results[stepId] = payload || {};
  },

  clearResults() {
    this.results = {};
  },

  // --- utilidades de serialización ---
  toJSON() {
    // orden por topología no es responsabilidad del estado;
    // devolvemos tal cual y el runner decidirá el orden
    return {
      version: '1.0.0',
      steps: this.steps.map(s => ({
        id: s.id,
        typeId: s.defId,
        nombre: s.label,
        position: { x: Math.round(s.pos.x), y: Math.round(s.pos.y) },
        props: s.props
      })),
      edges: this.edges.map(e => ({ from: e.from.step, to: e.to.step })),
    };
  },

  loadJSON(flow) {
    this.steps = [];
    this.edges = [];
    this.seq = 1;
    this.selectedStepId = null;
    this.lastStepId = null;
    this.clearResults();

    const steps = Array.isArray(flow?.steps) ? flow.steps : [];
    // reconstruir steps
    steps.forEach(st => {
      const id = st.id || `step_${this.seq++}`;
      this.steps.push({
        id,
        defId: st.typeId,
        label: st.nombre || st.typeId,
        categoria: st.categoria || 'proceso',
        pos: { x: st.position?.x ?? 40, y: st.position?.y ?? 40 },
        props: { ...(st.props || {}) },
        ports: { in: ['W','N'], out: ['E','S'] },
      });
      this.lastStepId = id;
    });

    // reconstruir edges válidos
    const valid = new Set(this.steps.map(s => s.id));
    const edges = Array.isArray(flow?.edges) ? flow.edges : [];
    this.edges = edges
      .filter(e => e && valid.has(e.from) && valid.has(e.to))
      .map(e => ({
        id: `edge_${Date.now()}_${Math.random().toString(36).slice(2,7)}`,
        from: { step: e.from, port: 'E' },
        to:   { step: e.to,   port: 'W' }
      }));
  },
};
