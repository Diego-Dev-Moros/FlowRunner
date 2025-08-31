# modules/funciones/archivos/lectura.py
import csv
import pandas as pd
from typing import List, Dict, Any

# Leer CSV → lista de dicts
def leer_csv(ruta_csv: str) -> List[Dict[str, Any]]:
    with open(ruta_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        if reader.fieldnames is None:
            # Si no hay encabezado, generamos campos genéricos
            csvfile.seek(0)
            raw_reader = csv.reader(csvfile)
            rows = list(raw_reader)
            if not rows:
                return []
            headers = [f"col{i+1}" for i in range(len(rows[0]))]
            return [dict(zip(headers, r)) for r in rows]
        return [row for row in reader]

# Leer Excel → lista de dicts
def leer_excel(ruta_excel: str, hoja: str):
    df = pd.read_excel(ruta_excel, sheet_name=hoja, engine='openpyxl')
    return df.to_dict(orient='records')

# Leer TXT delimitado → lista de dicts
def leer_txt_delimitado(ruta_txt: str, delimitador: str):
    with open(ruta_txt, 'r', encoding='utf-8') as f:
        # Intentar DictReader (requiere encabezado). Si falla, convertir manualmente.
        sample = f.read(4096)
        f.seek(0)
        sniffer = csv.Sniffer()
        try:
            has_header = sniffer.has_header(sample)
        except Exception:
            has_header = True
        if has_header:
            reader = csv.DictReader(f, delimiter=delimitador)
            return [row for row in reader]
        else:
            r = csv.reader(f, delimiter=delimitador)
            rows = list(r)
            if not rows:
                return []
            headers = [f"col{i+1}" for i in range(len(rows[0]))]
            return [dict(zip(headers, row)) for row in rows]

# # Main de prueba
# def main():
#     user_PC = getpass.getuser()

#     ruta_csv = fr"C:\Users\{user_PC}\OneDrive - PwC\ITC IT Seniors - Equipo 5\Archivos ejemplo\extracted_invoice_data.csv"
#     ruta_excel = fr"C:\Users\{user_PC}\OneDrive - PwC\ITC IT Seniors - Equipo 5\Archivos ejemplo\Reporte general.xlsx"
#     ruta_txt = fr"C:\Users\{user_PC}\OneDrive - PwC\ITC IT Seniors - Equipo 5\Archivos ejemplo\archivo_delimitado.txt"

#     print("CSV:")
#     print(leer_csv(ruta_csv)[:2])  # Mostrar primeros 2 registros

#     print("\nExcel:")
#     print(leer_excel(ruta_excel, "Reporte")[:2])

#     print("\nTXT:")
#     print(leer_txt_delimitado(ruta_txt, ",")[:2])

# if __name__ == "__main__":
#     main()