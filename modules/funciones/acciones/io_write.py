# modules/funciones/acciones/io_write.py
from __future__ import annotations
from typing import Any, Dict, List
import os
import csv

try:
    import pandas as pd  # opcional; sólo si usas escribir_excel
except Exception:
    pd = None


def escribir_csv(ctx, nombre_variable: str, ruta_destino: str):
    """
    Escribe en CSV los datos guardados en el contexto bajo 'nombre_variable'.
    Soporta: list[str], list[list], list[dict], dict, str/num.
    Crea carpetas si no existen.
    """
    if not ruta_destino:
        raise ValueError("Ruta de salida vacía.")

    data = ctx.obtener_variable(nombre_variable)
    if data is None:
        # Por si el usuario pasó accidentalmente un dato directo, escribirlo igual
        data = nombre_variable

    ruta_destino = os.path.expanduser(ruta_destino)
    os.makedirs(os.path.dirname(ruta_destino) or ".", exist_ok=True)

    rows_written = 0
    with open(ruta_destino, "w", newline="", encoding="utf-8") as f:
        if isinstance(data, list) and data and isinstance(data[0], dict):
            # lista de dicts
            cols = sorted({k for row in data for k in row.keys()})
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for row in data:
                w.writerow({k: row.get(k, "") for k in cols})
            rows_written = len(data)

        else:
            w = csv.writer(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, (list, tuple)):
                        w.writerow(list(item))
                    else:
                        w.writerow([item])
                rows_written = len(data)

            elif isinstance(data, dict):
                w.writerow(["key", "value"])
                for k, v in data.items():
                    w.writerow([k, v])
                rows_written = len(data)

            else:  # escalar / string
                w.writerow([data])
                rows_written = 1

    return {"path": ruta_destino, "rows": rows_written}


# (Opcionales, por si ya los estás usando en otros flujos)
def escribir_txt(ctx, nombre_variable: str, ruta_destino: str, delimitador: str = ","):
    data = ctx.obtener_variable(nombre_variable)
    if data is None:
        data = nombre_variable
    ruta_destino = os.path.expanduser(ruta_destino)
    os.makedirs(os.path.dirname(ruta_destino) or ".", exist_ok=True)

    with open(ruta_destino, "w", encoding="utf-8") as f:
        if isinstance(data, list):
            for item in data:
                if isinstance(item, (list, tuple)):
                    f.write(delimitador.join(map(str, item)) + "\n")
                else:
                    f.write(str(item) + "\n")
        elif isinstance(data, dict):
            for k, v in data.items():
                f.write(f"{k}{delimitador}{v}\n")
        else:
            f.write(str(data))
    return {"path": ruta_destino}


def escribir_excel(ctx, nombre_variable: str, ruta_destino: str, hoja: str = "Hoja1"):
    """
    Muy básico; requiere pandas. Convierte a DataFrame en los casos comunes.
    """
    if pd is None:
        raise RuntimeError("pandas no está instalado. Requerido para escribir Excel.")

    data = ctx.obtener_variable(nombre_variable)
    if data is None:
        data = nombre_variable

    ruta_destino = os.path.expanduser(ruta_destino)
    os.makedirs(os.path.dirname(ruta_destino) or ".", exist_ok=True)

    # List[dict] → DataFrame
    if isinstance(data, list) and data and isinstance(data[0], dict):
        df = pd.DataFrame(data)
    elif isinstance(data, list):
        df = pd.DataFrame({"value": data})
    elif isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=["key", "value"])
    else:
        df = pd.DataFrame({"value": [data]})

    with pd.ExcelWriter(ruta_destino, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=hoja)

    return {"path": ruta_destino, "rows": len(df)}
