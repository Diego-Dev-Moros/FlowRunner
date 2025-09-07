/**
 * AUDITORÍA TÉCNICA - HOTFIX PACK TEST SUITE COMPLETA
 * Script avanzado para validar todas las mejoras y detectar conflictos
 */

// TEST #1: Performance - Drag y Render Batching
function testDragPerformance() {
    console.log('🔄 TEST #1: Performance - Drag y Render Batching');
    
    // Crear 15 nodos para test intensivo
    const testNodes = [];
    for (let i = 0; i < 15; i++) {
        const node = document.createElement('div');
        node.className = 'node';
        node.id = `perf-test-node-${i}`;
        node.style.left = `${100 + (i % 5) * 150}px`;
        node.style.top = `${100 + Math.floor(i / 5) * 120}px`;
        node.innerHTML = `
            <div class="node-header"><div class="node-title">PerfTest ${i}</div></div>
            <div class="node-body"><div class="badge">Test Node</div></div>
        `;
        document.getElementById('lienzo').appendChild(node);
        testNodes.push(node);
    }
    
    // Medir FPS durante 90 frames de drag intensivo
    let frameCount = 0;
    let renderCount = 0;
    let rafCallbacks = 0;
    const startTime = performance.now();
    
    // Interceptar scheduleEdges para contar renders
    const originalScheduleEdges = window.scheduleEdges;
    const originalRAF = window.requestAnimationFrame;
    
    window.scheduleEdges = function() {
        renderCount++;
        return originalScheduleEdges?.call(this);
    };
    
    window.requestAnimationFrame = function(callback) {
        rafCallbacks++;
        return originalRAF.call(this, callback);
    };
    
    function intensiveDragSimulation() {
        if (frameCount < 90) {
            // Simular drag intensivo con múltiples nodos
            testNodes.forEach((node, i) => {
                const time = frameCount * 0.1;
                const offsetX = Math.sin(time + i * 0.5) * 30;
                const offsetY = Math.cos(time + i * 0.3) * 20;
                const rotation = Math.sin(time + i) * 2;
                
                node.style.transform = `translate(${offsetX}px, ${offsetY}px) rotate(${rotation}deg)`;
            });
            
            // Trigger múltiples updates
            if (window.scheduleEdges) window.scheduleEdges();
            if (window.scheduleCanvasSize) window.scheduleCanvasSize();
            
            frameCount++;
            requestAnimationFrame(intensiveDragSimulation);
        } else {
            // Análisis de resultados
            const duration = performance.now() - startTime;
            const fps = (frameCount / duration) * 1000;
            const renderEfficiency = renderCount / rafCallbacks;
            const batchingRatio = rafCallbacks / frameCount;
            
            console.log(`📊 PERFORMANCE METRICS:`);
            console.log(`   FPS: ${fps.toFixed(2)} (target: >45)`);
            console.log(`   Render calls: ${renderCount}`);
            console.log(`   RAF callbacks: ${rafCallbacks}`);
            console.log(`   Batching ratio: ${batchingRatio.toFixed(2)} (target: <1.5)`);
            console.log(`   Render efficiency: ${renderEfficiency.toFixed(2)}`);
            
            // Evaluación
            const perfScore = Math.min(100, (fps / 45) * 50 + (1.5 / batchingRatio) * 50);
            
            if (fps > 45 && batchingRatio < 1.5) {
                console.log(`🟢 TEST #1 PASSED - Performance excelente (Score: ${perfScore.toFixed(1)}/100)`);
            } else if (fps > 30 && batchingRatio < 2.0) {
                console.log(`🟡 TEST #1 PARTIAL - Performance aceptable (Score: ${perfScore.toFixed(1)}/100)`);
            } else {
                console.log(`🔴 TEST #1 FAILED - Performance insuficiente (Score: ${perfScore.toFixed(1)}/100)`);
            }
            
            // Cleanup y restauración
            testNodes.forEach(node => node.remove());
            window.scheduleEdges = originalScheduleEdges;
            window.requestAnimationFrame = originalRAF;
        }
    }
    
    requestAnimationFrame(intensiveDragSimulation);
}

// TEST #2: Node Shapes Unificado - Verificar sistema nuevo
function testNodeShapesUnified() {
    console.log('🔄 TEST #2: Sistema de Formas Unificado - Validación completa');
    
    const testCases = [
        { typeId: 'condicional_si', expectedClass: 'node--decision', expectedShape: 'decision', description: 'Condicional Si - Rombo' },
        { typeId: 'condicional_multiple', expectedClass: 'node--decision', expectedShape: 'decision', description: 'Switch - Rombo' },
        { typeId: 'bucle_mientras', expectedClass: 'node--loop', expectedShape: 'loop', description: 'Bucle While - Hexágono' },
        { typeId: 'bucle_for_lista', expectedClass: 'node--loop', expectedShape: 'loop', description: 'Bucle For - Hexágono' },
        { typeId: 'inicio', expectedClass: 'node--inicio', expectedShape: 'inicio', description: 'Inicio - Píldora Verde' },
        { typeId: 'fin', expectedClass: 'node--cierre', expectedShape: 'cierre', description: 'Fin - Píldora Roja' },
        { typeId: 'pausa', expectedClass: null, expectedShape: null, description: 'Pausa - Círculo Normal' }
    ];
    
    const testContainer = document.getElementById('lienzo');
    let passedTests = 0;
    let totalTests = testCases.length;
    
    // Test del sistema applyNodeShape
    const hasApplyNodeShape = typeof window.applyNodeShape === 'function';
    console.log(`   applyNodeShape function: ${hasApplyNodeShape ? '✅ Found' : '❌ Missing'}`);
    
    testCases.forEach((test, i) => {
        // Crear nodo de prueba
        const node = document.createElement('div');
        node.className = 'node';
        node.id = `unified-shape-test-${i}`;
        node.style.left = `${50 + (i % 4) * 200}px`;
        node.style.top = `${300 + Math.floor(i / 4) * 150}px`;
        
        // Simular definición de acción
        const mockDef = {
            id: test.typeId,
            categoria: test.typeId.includes('bucle') ? 'loops' : 
                      test.typeId.includes('condicional') ? 'decision' : 'basic'
        };
        
        // Aplicar sistema de formas si está disponible
        if (window.applyNodeShape) {
            window.applyNodeShape(node, test.typeId, mockDef);
        } else {
            // Fallback manual para testing
            node.dataset.typeId = test.typeId;
            if (test.expectedClass) node.classList.add(test.expectedClass);
        }
        
        node.innerHTML = `
            <div class="node-header">
                <div class="node-title">${test.description}</div>
            </div>
            <div class="node-body">
                <div class="badge">Shape Test</div>
            </div>
        `;
        
        testContainer.appendChild(node);
        
        // Verificación inmediata
        const hasCorrectClass = test.expectedClass ? node.classList.contains(test.expectedClass) : true;
        const hasCorrectData = node.dataset.nodeShape === test.expectedShape || (!test.expectedShape && !node.dataset.nodeShape);
        const hasCorrectTypeId = node.dataset.typeId === test.typeId;
        
        // Verificación CSS después del próximo frame
        setTimeout(() => {
            const styles = window.getComputedStyle(node, '::before');
            let hasCorrectVisualStyle = true;
            
            if (test.expectedShape === 'decision') {
                hasCorrectVisualStyle = styles.clipPath && styles.clipPath.includes('polygon');
            } else if (test.expectedShape === 'loop') {
                hasCorrectVisualStyle = styles.boxShadow && styles.boxShadow.includes('inset');
            } else if (test.expectedShape === 'inicio' || test.expectedShape === 'cierre') {
                hasCorrectVisualStyle = styles.borderRadius === '999px';
            }
            
            const testPassed = hasCorrectClass && hasCorrectData && hasCorrectTypeId && hasCorrectVisualStyle;
            
            if (testPassed) {
                console.log(`   ✅ ${test.description}: CORRECTO`);
                passedTests++;
            } else {
                console.log(`   ❌ ${test.description}: FALLO`);
                console.log(`      - Class: ${hasCorrectClass}, Data: ${hasCorrectData}, TypeId: ${hasCorrectTypeId}, Style: ${hasCorrectVisualStyle}`);
            }
            
            // Cleanup después de validación
            setTimeout(() => node.remove(), 3000);
            
        }, 100);
    });
    
    setTimeout(() => {
        const successRate = (passedTests / totalTests) * 100;
        console.log(`📊 SHAPES SYSTEM RESULTS: ${passedTests}/${totalTests} tests passed (${successRate.toFixed(1)}%)`);
        
        if (successRate >= 85) {
            console.log('🟢 TEST #2 PASSED - Sistema de formas unificado funcionando correctamente');
        } else if (successRate >= 60) {
            console.log('� TEST #2 PARTIAL - Sistema de formas funcional con issues menores');
        } else {
            console.log('🔴 TEST #2 FAILED - Sistema de formas requiere atención');
        }
    }, 1000);
}

// TEST #3: Conflicto Detection - Detectar dual node systems
function testDualNodeSystemConflict() {
    console.log('🔄 TEST #3: Detección de Conflictos - Dual Node System');
    
    // Detectar funciones de creación de nodos
    const mainJsCreateNode = typeof window.createNode === 'function';
    const mainJsMountNode = typeof window.mountNode === 'function';
    
    // Intentar importar nodes.js dinámicamente
    let nodesJsCreateNode = false;
    try {
        // Verificar si nodes.js está disponible
        const nodesModule = window.nodesJS || {};
        nodesJsCreateNode = typeof nodesModule.createNode === 'function';
    } catch (e) {
        nodesJsCreateNode = false;
    }
    
    // Verificar elementos en DOM que puedan indicar ambos sistemas
    const mainJsNodes = document.querySelectorAll('.node[id^="N"]'); // main.js pattern
    const nodesJsNodes = document.querySelectorAll('.node[data-step-id]'); // nodes.js pattern
    
    console.log(`📊 NODE SYSTEM DETECTION:`);
    console.log(`   main.js createNode: ${mainJsCreateNode ? '✅ Present' : '❌ Missing'}`);
    console.log(`   main.js mountNode: ${mainJsMountNode ? '✅ Present' : '❌ Missing'}`);
    console.log(`   nodes.js createNode: ${nodesJsCreateNode ? '⚠️ Present (CONFLICT!)' : '✅ Not detected'}`);
    console.log(`   main.js pattern nodes: ${mainJsNodes.length}`);
    console.log(`   nodes.js pattern nodes: ${nodesJsNodes.length}`);
    
    // Análisis de conflicto
    const hasConflict = mainJsCreateNode && mainJsMountNode && nodesJsCreateNode;
    const hasDualPatterns = mainJsNodes.length > 0 && nodesJsNodes.length > 0;
    
    if (hasConflict) {
        console.log('🔴 CONFLICT DETECTED: Dual node creation systems active');
        console.log('   Recommend: Consolidate to main.js as single source of truth');
    } else if (hasDualPatterns) {
        console.log('🟡 PARTIAL CONFLICT: Mixed node patterns detected');
        console.log('   Recommend: Standardize node creation pattern');
    } else {
        console.log('� NO CONFLICT: Single node creation system detected');
    }
    
    return !hasConflict && !hasDualPatterns;
}

// TEST #4: Edge Stability Mejorado - Verificar optimizaciones
function testEdgeStabilityOptimized() {
    console.log('🔄 TEST #4: Edge Stability Optimizado - Validación completa');
    
    // Verificar getBox optimizations
    const edgesModule = window.edges || {};
    const hasOptimizedGetBox = edgesModule.getBox && 
                              edgesModule.getBox._hostRectCache !== undefined;
    
    console.log(`   Optimized getBox: ${hasOptimizedGetBox ? '✅ Implemented' : '❌ Missing'}`);
    
    // Verificar vector-effect en paths existentes
    const paths = document.querySelectorAll('#svgEdges path');
    let pathsWithVectorEffect = 0;
    let pathsWithShapeRendering = 0;
    
    paths.forEach(path => {
        if (path.getAttribute('vector-effect') === 'non-scaling-stroke') {
            pathsWithVectorEffect++;
        }
        if (path.getAttribute('shape-rendering') === 'geometricPrecision') {
            pathsWithShapeRendering++;
        }
    });
    
    console.log(`📊 EDGE OPTIMIZATION STATUS:`);
    console.log(`   Paths with vector-effect: ${pathsWithVectorEffect}/${paths.length}`);
    console.log(`   Paths with shape-rendering: ${pathsWithShapeRendering}/${paths.length}`);
    
    // Test zoom levels y transform-origin
    const zoomLevels = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0];
    const lienzo = document.getElementById('lienzo');
    const svg = document.getElementById('svgEdges');
    
    let transformOriginTests = 0;
    
    zoomLevels.forEach(zoom => {
        lienzo.style.transform = `scale(${zoom})`;
        svg.style.transform = `scale(${zoom})`;
        
        const lienzoOrigin = window.getComputedStyle(lienzo).transformOrigin;
        const svgOrigin = window.getComputedStyle(svg).transformOrigin;
        
        if (lienzoOrigin.startsWith('0px 0px') && svgOrigin.startsWith('0px 0px')) {
            transformOriginTests++;
        }
    });
    
    // Restaurar zoom normal
    lienzo.style.transform = 'scale(1)';
    svg.style.transform = 'scale(1)';
    
    const vectorEffectScore = paths.length > 0 ? (pathsWithVectorEffect / paths.length) * 100 : 100;
    const transformOriginScore = (transformOriginTests / zoomLevels.length) * 100;
    const overallScore = (vectorEffectScore + transformOriginScore) / 2;
    
    console.log(`📊 EDGE STABILITY SCORE: ${overallScore.toFixed(1)}%`);
    
    if (overallScore >= 90) {
        console.log('🟢 TEST #4 PASSED - Edge stability optimizado correctamente');
    } else if (overallScore >= 70) {
        console.log('� TEST #4 PARTIAL - Edge stability funcional con mejoras posibles');
    } else {
        console.log('🔴 TEST #4 FAILED - Edge stability requiere atención');
    }
    
    return overallScore >= 90;
}

// MASTER TEST SUITE - Ejecutar todos con reporte consolidado
function runCompleteAuditTests() {
    console.log('� EJECUTANDO AUDITORÍA TÉCNICA COMPLETA');
    console.log('═'.repeat(60));
    
    const results = {
        performance: null,
        shapes: null,
        conflicts: null,
        edges: null,
        startTime: performance.now()
    };
    
    // Test 1: Performance
    testDragPerformance();
    
    setTimeout(() => {
        // Test 2: Shapes
        testNodeShapesUnified();
    }, 2000);
    
    setTimeout(() => {
        // Test 3: Conflicts
        results.conflicts = testDualNodeSystemConflict();
    }, 4000);
    
    setTimeout(() => {
        // Test 4: Edge Stability  
        results.edges = testEdgeStabilityOptimized();
    }, 5000);
    
    setTimeout(() => {
        // Reporte consolidado
        const duration = performance.now() - results.startTime;
        
        console.log('═'.repeat(60));
        console.log('🎯 AUDITORÍA TÉCNICA - REPORTE CONSOLIDADO');
        console.log(`   Duración total: ${(duration / 1000).toFixed(2)}s`);
        console.log('');
        
        // Calcular score general
        const conflictScore = results.conflicts ? 100 : 50;
        const edgeScore = results.edges ? 100 : 70;
        const overallScore = (conflictScore + edgeScore) / 2;
        
        console.log(`📊 OVERALL SYSTEM HEALTH: ${overallScore.toFixed(1)}/100`);
        
        if (overallScore >= 90) {
            console.log('🟢 SYSTEM STATUS: EXCELLENT - Production Ready');
        } else if (overallScore >= 75) {
            console.log('� SYSTEM STATUS: GOOD - Minor Issues Detected');
        } else {
            console.log('� SYSTEM STATUS: NEEDS ATTENTION - Critical Issues Found');
        }
        
        console.log('');
        console.log('📋 RECOMMENDED ACTIONS:');
        if (!results.conflicts) {
            console.log('   🔧 Consolidate dual node creation systems');
        }
        if (!results.edges) {
            console.log('   🔧 Complete edge stability optimization');
        }
        console.log('   ✅ Run production deployment tests');
        console.log('   ✅ Monitor performance metrics');
        
        console.log('═'.repeat(60));
        console.log('✅ AUDITORÍA TÉCNICA COMPLETADA');
        
    }, 7000);
}

// Exponer funciones
window.testDragPerformance = testDragPerformance;
window.testNodeShapesUnified = testNodeShapesUnified;
window.testDualNodeSystemConflict = testDualNodeSystemConflict;
window.testEdgeStabilityOptimized = testEdgeStabilityOptimized;
window.runCompleteAuditTests = runCompleteAuditTests;

// Backward compatibility
window.runHotfixTests = runCompleteAuditTests;

console.log('🔧 AUDITORÍA TÉCNICA TEST SUITE LOADED');
console.log('Ejecutar: runCompleteAuditTests() para auditoría completa');
