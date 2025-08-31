# modules/funciones/archivos/escritura.py
import os
import csv
from typing import Any, List, Dict
import pandas as pd

def _ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def _as_records(data: Any) -> List[Dict]:
    """Convierte data a lista de dicts si es posible."""
    if data is None:
        return []
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient='records')
    if isinstance(data, list):
        if not data:
            return []
        if isinstance(data[0], dict):
            return data  # ya está OK
        if isinstance(data[0], (list, tuple)):
            # Convertir a dicts generando columnas genéricas
            maxlen = max(len(row) for row in data)
            headers = [f"col{i+1}" for i in range(maxlen)]
            return [dict(zip(headers, row)) for row in data]
        if isinstance(data[0], str):
            # Para TXT, lo manejamos distinto fuera
            return [{"value": v} for v in data]
    if isinstance(data, dict):
        # Un solo dict → lista de uno
        return [data]
    # Cualquier otro → DataFrame y luego records
    try:
        return pd.DataFrame(data).to_dict(orient='records')
    except Exception:
        return [{"value": str(data)}]

def escribir_csv(data: Any, ruta: str):
    _ensure_dir(ruta)
    records = _as_records(data)
    if not records:
        # Crear archivo vacío con headers vacíos
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            pass
        return ruta
    headers = sorted({k for row in records for k in row.keys()})
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in records:
            writer.writerow({k: row.get(k, "") for k in headers})
    return ruta

def escribir_excel(data: Any, ruta: str, hoja: str = "Hoja1"):
    _ensure_dir(ruta)
    if isinstance(data, pd.DataFrame):
        df = data
    else:
        records = _as_records(data)
        df = pd.DataFrame(records)
    with pd.ExcelWriter(ruta, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=hoja)
    return ruta

def escribir_txt(data: Any, ruta: str, delimitador: str = ','):
    _ensure_dir(ruta)
    # Si es list[str], grabar línea a línea
    if isinstance(data, list) and data and isinstance(data[0], str):
        with open(ruta, 'w', encoding='utf-8') as f:
            for line in data:
                f.write(line.rstrip('\n') + '\n')
        return ruta

    # Si es estructura tabular → separar por delimitador
    records = _as_records(data)
    if not records:
        with open(ruta, 'w', encoding='utf-8') as f:
            pass
        return ruta

    headers = sorted({k for row in records for k in row.keys()})
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(delimitador.join(headers) + '\n')
        for row in records:
            values = [str(row.get(h, "")) for h in headers]
            f.write(delimitador.join(values) + '\n')
    return ruta