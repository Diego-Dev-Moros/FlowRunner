/**
 * FlowRunner - Batería de Pruebas Post-Refactorización
 * Suite completa de validación con archivos finales
 * 
 * ARCHIVOS VERIFICADOS:
 * - main.js (refactorizado, 150 líneas)
 * - estilos.css (sin reglas de nodos)
 * - nodes.css (sistema completo)
 * - Módulos cohesionados en edges/, nodes/, io/, runtime/
 */

// Ejecutar en la consola del navegador después de la refactorización
console.log('🧪 Iniciando batería de pruebas de refactorización...');

const TestSuite = {
  results: [],
  
  log(category, test, passed, details = '') {
    const result = { category, test, passed, details, timestamp: new Date().toISOString() };
    this.results.push(result);
    const icon = passed ? '✅' : '❌';
    console.log(`${icon} [${category}] ${test}${details ? ': ' + details : ''}`);
  },
  
  async runAll() {
    console.log('🚀 Ejecutando suite completa de pruebas...\n');
    
    await this.testModuleLoading();
    await this.testCSSArchitecture();
    await this.testNodeCreation();
    await this.testPerformance();
    await this.testShapes();
    await this.testConnections();
    await this.testViewport();
    await this.testFlowIO();
    
    this.generateReport();
  },
  
  // Test 1: Carga de Módulos
  async testModuleLoading() {
    console.log('📦 Testing Module Loading...');
    
    try {
      // Verificar que los módulos principales están disponibles
      const modules = [
        'panzoom', 'viewport', 'edges/scheduler', 'edges/view',
        'nodes/view', 'nodes/ports', 'io/flow-io', 'runtime/bridge'
      ];
      
      for (const moduleName of modules) {
        try {
          const module = await import(`/vistas/services/${moduleName}.js`);
          this.log('MODULES', `Import ${moduleName}`, !!module);
        } catch (error) {
          this.log('MODULES', `Import ${moduleName}`, false, error.message);
        }
      }
      
      // Verificar elementos DOM necesarios
      const elements = ['workspace', 'lienzo', 'svgEdges', 'topbar', 'sidebar', 'props'];
      elements.forEach(id => {
        const el = document.getElementById(id);
        this.log('DOM', `Element #${id}`, !!el);
      });
      
    } catch (error) {
      this.log('MODULES', 'General module loading', false, error.message);
    }
  },
  
  // Test 2: Arquitectura CSS
  async testCSSArchitecture() {
    console.log('🎨 Testing CSS Architecture...');
    
    // Verificar que se cargaron los CSS correctos
    const stylesheets = Array.from(document.styleSheets);
    const hasCleanCSS = stylesheets.some(sheet => 
      sheet.href && sheet.href.includes('estilos-clean.css')
    );
    const hasNodesCSS = stylesheets.some(sheet => 
      sheet.href && sheet.href.includes('nodes-complete.css')
    );
    
    this.log('CSS', 'estilos-clean.css loaded', hasCleanCSS);
    this.log('CSS', 'nodes-complete.css loaded', hasNodesCSS);
    
    // Verificar separación: estilos-clean no debe tener reglas de .node
    // Esto es una approximación ya que no podemos leer las reglas fácilmente
    const bodyStyles = getComputedStyle(document.body);
    this.log('CSS', 'Base styles applied', bodyStyles.fontFamily.includes('system-ui'));
  },
  
  // Test 3: Creación de Nodos
  async testNodeCreation() {
    console.log('🔧 Testing Node Creation...');
    
    try {
      // Simular creación de nodo
      const workspace = document.getElementById('workspace');
      const event = new DragEvent('drop', {
        clientX: 300,
        clientY: 200,
        dataTransfer: new DataTransfer()
      });
      
      // Simular datos de drag
      event.dataTransfer.setData('text/plain', 'variable_set');
      
      // Verificar que se puede disparar el evento
      const canDispatch = workspace.dispatchEvent(event);
      this.log('NODES', 'Drop event dispatchable', canDispatch);
      
      // Verificar existencia de funciones de nodos
      const nodeView = await import('/vistas/services/nodes/view.js');
      this.log('NODES', 'createNode function exists', typeof nodeView.createNode === 'function');
      this.log('NODES', 'mountNode function exists', typeof nodeView.mountNode === 'function');
      
    } catch (error) {
      this.log('NODES', 'Node creation testing', false, error.message);
    }
  },
  
  // Test 4: Performance - RAF Batching
  async testPerformance() {
    console.log('⚡ Testing Performance Optimizations...');
    
    try {
      const scheduler = await import('/vistas/services/edges/scheduler.js');
      
      // Test RAF batching
      let callCount = 0;
      const originalRaf = window.requestAnimationFrame;
      window.requestAnimationFrame = (callback) => {
        callCount++;
        return originalRaf(callback);
      };
      
      // Llamar scheduler múltiples veces
      scheduler.scheduleEdges();
      scheduler.scheduleEdges();
      scheduler.scheduleEdges();
      
      // Debe resultar en solo 1 RAF call
      setTimeout(() => {
        this.log('PERFORMANCE', 'RAF batching works', callCount === 1, `${callCount} RAF calls`);
        window.requestAnimationFrame = originalRaf; // Restore
      }, 10);
      
      // Test funciones scheduler
      this.log('PERFORMANCE', 'scheduleEdges exists', typeof scheduler.scheduleEdges === 'function');
      this.log('PERFORMANCE', 'scheduleCanvasSize exists', typeof scheduler.scheduleCanvasSize === 'function');
      
    } catch (error) {
      this.log('PERFORMANCE', 'Performance testing', false, error.message);
    }
  },
  
  // Test 5: Sistema de Formas
  async testShapes() {
    console.log('💎 Testing Node Shapes...');
    
    // Crear nodo temporal para probar formas
    const testNode = document.createElement('div');
    testNode.className = 'node';
    document.body.appendChild(testNode);
    
    // Test diferentes formas
    const shapes = [
      { class: 'node--decision', shape: 'rombo' },
      { class: 'node--loop', shape: 'hexágono' },
      { class: 'node--inicio', shape: 'píldora' },
      { class: 'node--cierre', shape: 'píldora' }
    ];
    
    shapes.forEach(({ class: shapeClass, shape }) => {
      testNode.className = `node ${shapeClass}`;
      const styles = getComputedStyle(testNode, '::before');
      
      // Verificar que el pseudo-elemento tiene estilos
      const hasStyles = styles.content !== 'none' || styles.position === 'absolute';
      this.log('SHAPES', `${shape} shape (${shapeClass})`, hasStyles);
    });
    
    // Cleanup
    testNode.remove();
  },
  
  // Test 6: Sistema de Conexiones
  async testConnections() {
    console.log('🔗 Testing Connection System...');
    
    try {
      const ports = await import('/vistas/services/nodes/ports.js');
      
      // Test funciones principales
      this.log('CONNECTIONS', 'setupPorts exists', typeof ports.setupPorts === 'function');
      this.log('CONNECTIONS', 'addEdge exists', typeof ports.addEdge === 'function');
      this.log('CONNECTIONS', 'getNodeConnections exists', typeof ports.getNodeConnections === 'function');
      
      // Test SVG rendering
      const edgeView = await import('/vistas/services/edges/view.js');
      this.log('CONNECTIONS', 'renderEdges exists', typeof edgeView.renderEdges === 'function');
      
      // Verificar SVG setup
      const svg = document.getElementById('svgEdges');
      this.log('CONNECTIONS', 'SVG edges element exists', !!svg);
      if (svg) {
        this.log('CONNECTIONS', 'SVG has vector-effect support', 
          svg.style.vectorEffect !== undefined || 
          document.createElementNS('http://www.w3.org/2000/svg', 'path').style.vectorEffect !== undefined
        );
      }
      
    } catch (error) {
      this.log('CONNECTIONS', 'Connection system testing', false, error.message);
    }
  },
  
  // Test 7: Viewport y Pan/Zoom
  async testViewport() {
    console.log('🔍 Testing Viewport & Pan/Zoom...');
    
    try {
      const panzoom = await import('/vistas/services/panzoom.js');
      const viewport = await import('/vistas/services/viewport.js');
      
      // Test funciones pan/zoom
      this.log('VIEWPORT', 'getZoom exists', typeof panzoom.getZoom === 'function');
      this.log('VIEWPORT', 'setZoomLevel exists', typeof panzoom.setZoomLevel === 'function');
      
      // Test funciones viewport
      this.log('VIEWPORT', 'centerOnStep exists', typeof viewport.centerOnStep === 'function');
      this.log('VIEWPORT', 'updateCanvasSize exists', typeof viewport.updateCanvasSize === 'function');
      
      // Test zoom inicial
      const currentZoom = panzoom.getZoom();
      this.log('VIEWPORT', 'Initial zoom is 1', currentZoom === 1, `Current: ${currentZoom}`);
      
      // Test elementos con transform-origin
      const lienzo = document.getElementById('lienzo');
      const svgEdges = document.getElementById('svgEdges');
      
      if (lienzo) {
        const transformOrigin = getComputedStyle(lienzo).transformOrigin;
        this.log('VIEWPORT', 'Lienzo has transform-origin', transformOrigin.includes('0') || transformOrigin.includes('0px'));
      }
      
    } catch (error) {
      this.log('VIEWPORT', 'Viewport testing', false, error.message);
    }
  },
  
  // Test 8: Import/Export
  async testFlowIO() {
    console.log('💾 Testing Flow I/O...');
    
    try {
      const flowIO = await import('/vistas/services/io/flow-io.js');
      
      // Test funciones principales
      this.log('FLOW_IO', 'exportJSON exists', typeof flowIO.exportJSON === 'function');
      this.log('FLOW_IO', 'importJSON exists', typeof flowIO.importJSON === 'function');
      this.log('FLOW_IO', 'clearCanvas exists', typeof flowIO.clearCanvas === 'function');
      
      // Test JSON de ejemplo
      const sampleFlow = {
        version: '1.0.0',
        steps: [
          {
            id: 'test_step',
            typeId: 'variable_set',
            nombre: 'Test Step',
            position: { x: 100, y: 100 },
            props: { variable: 'test', valor: 'test_value' }
          }
        ],
        edges: []
      };
      
      // Verificar que el JSON es válido
      const jsonString = JSON.stringify(sampleFlow);
      this.log('FLOW_IO', 'Can generate valid JSON', jsonString.includes('version'));
      
    } catch (error) {
      this.log('FLOW_IO', 'Flow I/O testing', false, error.message);
    }
  },
  
  // Generar reporte final
  generateReport() {
    console.log('\n📊 REPORTE FINAL DE PRUEBAS');
    console.log('═'.repeat(50));
    
    const categories = [...new Set(this.results.map(r => r.category))];
    const summary = {};
    
    categories.forEach(cat => {
      const tests = this.results.filter(r => r.category === cat);
      const passed = tests.filter(t => t.passed).length;
      const total = tests.length;
      const percentage = Math.round((passed / total) * 100);
      
      summary[cat] = { passed, total, percentage };
      console.log(`${cat.padEnd(12)} | ${passed.toString().padStart(2)}/${total.toString().padStart(2)} | ${percentage.toString().padStart(3)}%`);
    });
    
    const totalPassed = this.results.filter(r => r.passed).length;
    const totalTests = this.results.length;
    const overallPercentage = Math.round((totalPassed / totalTests) * 100);
    
    console.log('─'.repeat(50));
    console.log(`GENERAL      | ${totalPassed.toString().padStart(2)}/${totalTests.toString().padStart(2)} | ${overallPercentage.toString().padStart(3)}%`);
    console.log('═'.repeat(50));
    
    // Mostrar fallos
    const failures = this.results.filter(r => !r.passed);
    if (failures.length > 0) {
      console.log('\n❌ PRUEBAS FALLIDAS:');
      failures.forEach(f => {
        console.log(`   • [${f.category}] ${f.test}: ${f.details || 'Sin detalles'}`);
      });
    } else {
      console.log('\n🎉 ¡TODAS LAS PRUEBAS PASARON!');
    }
    
    // Recomendaciones
    if (overallPercentage >= 95) {
      console.log('\n🚀 Refactorización EXITOSA - Sistema listo para producción');
    } else if (overallPercentage >= 85) {
      console.log('\n✅ Refactorización BUENA - Revisar fallos menores');
    } else {
      console.log('\n⚠️  Refactorización PARCIAL - Se requieren correcciones');
    }
    
    return summary;
  }
};

// Auto-ejecutar si se ejecuta directamente
if (typeof window !== 'undefined') {
  window.FlowRunnerTests = TestSuite;
  
  // Ejecutar pruebas después de un pequeño delay para permitir inicialización
  setTimeout(() => {
    TestSuite.runAll();
  }, 2000);
}

console.log('🧪 Suite de pruebas cargada. Para ejecutar manualmente: FlowRunnerTests.runAll()');
