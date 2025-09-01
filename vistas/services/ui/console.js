export function setupConsole({ onRun, onStop, onClear }) {
  const el = document.getElementById('console');
  el.innerHTML = `
    <div class="con-header">
      <div class="con-title">Flow Console</div>
      <div class="con-actions">
        <button id="con-run">▶ Ejecutar</button>
        <button id="con-stop">■ Detener</button>
        <button id="con-clear">🧹 Limpiar</button>
      </div>
    </div>
    <div class="con-body" id="con-body"></div>
  `;

  el.querySelector('#con-run').addEventListener('click', onRun);
  el.querySelector('#con-stop').addEventListener('click', onStop);
  el.querySelector('#con-clear').addEventListener('click', () => {
    const body = el.querySelector('#con-body'); body.innerHTML = ''; onClear?.();
  });

  const body = el.querySelector('#con-body');

  function line(kind, msg) {
    const row = document.createElement('div');
    row.className = `con-line ${kind}`;
    // si msg es objeto, serializa
    const text = (typeof msg === 'string') ? msg : JSON.stringify(msg, null, 2);
    row.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
    body.appendChild(row);
    body.scrollTop = body.scrollHeight;
  }

  return {
    log: (m) => line('log', m),
    ok:  (m) => line('ok',  m),
    err: (m) => line('err', m),
    stepStart: (step) => line('step', `▶ ${step.label} (${step.id})`),
    stepEnd:   (step, res) => line('ok',  `✔ ${step.label}: ${short(res)}`),
    stepFail:  (step, e)   => line('err', `✖ ${step.label}: ${e?.message || e}`),
    clear: () => { body.innerHTML = ''; }
  };
}

function short(res) {
  if (res == null) return 'OK';
  const s = typeof res === 'string' ? res : JSON.stringify(res);
  return s.length > 140 ? s.slice(0, 140) + '…' : s;
}
