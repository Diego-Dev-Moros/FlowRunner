#!/usr/bin/env python3
# test_registry.py
from modules.actions import *
from modules.core import ActionRegistry

print('=== PRUEBA DE REGISTRO DE ACCIONES ===')
print(f'Acciones registradas: {len(ActionRegistry._actions)}')
print(f'Categorías: {list(ActionRegistry._categories.keys())}')

print('\n=== ACCIONES DETALLADAS ===')
for k, v in ActionRegistry._actions.items():
    print(f'  {k}: {v.name} ({v.category})')

print('\n=== POR CATEGORÍAS ===')
for cat, actions in ActionRegistry._categories.items():
    print(f'{cat}:')
    for action in actions:
        print(f'  - {action.id}: {action.name}')
