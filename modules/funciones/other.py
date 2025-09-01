import os

# Carpetas que se deben ignorar
ignored_dirs = {'.venv'}

def generate_tree_structure(directory, prefix=""):
    tree_structure = ""
    try:
        entries = sorted(os.listdir(directory))
    except FileNotFoundError:
        return f"Error: La ruta '{directory}' no existe.\n"

    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        if os.path.isdir(path) and entry in ignored_dirs:
            continue
        connector = "├─ " if index < len(entries) - 1 else "└─ "
        tree_structure += f"{prefix}{connector}{entry}\n"
        if os.path.isdir(path):
            extension = "│   " if index < len(entries) - 1 else "    "
            tree_structure += generate_tree_structure(path, prefix + extension)
    return tree_structure

# Ruta del directorio que querés analizar
directory_path = r"C:\Users\Diego\Desktop\ProyectoF\FlowRunner"

# Generar la estructura
estructura = generate_tree_structure(directory_path)

# Guardar en archivo .txt
with open("estructura_directorio.txt", "w", encoding="utf-8") as archivo:
    archivo.write(estructura)

print("La estructura se guardó en 'estructura_directorio.txt'.")