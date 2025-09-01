# Crear entorno virtual y activar
py -m venv .venv; .venv/scripts/activate; pip install -r requirements.txt

# Activar entorno
.venv/scripts/activate

# Crear paquete para usar.

## Crear ejecutable;
python -m eel index.py web -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole

## Si pyinstaller está en versión > 6.0 agregar:
--contents-directory .

## Quedaría:
python -m eel index.py web -n ToolKit --copy-metadata pikepdf --collect-data docxcompose --noconsole --contents-directory .

