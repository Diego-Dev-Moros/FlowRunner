# modules/utils/dialogs.py
"""
Utilidades consolidadas para diálogos de usuario.
"""
from typing import Tuple, List


def seleccionar_archivo(titulo: str = "Seleccionar archivo", 
                       tipos: Tuple[Tuple[str, str], ...] = (("Todos", "*.*"),)) -> str:
    """Abre un diálogo para seleccionar un archivo."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        root.attributes('-topmost', True)  # Mantener al frente
        
        fname = filedialog.askopenfilename(title=titulo, filetypes=tipos)
        
        root.update()
        root.destroy()
        
        return fname or ""
        
    except Exception as e:
        print(f"Error en diálogo de archivo: {e}")
        return ""


def seleccionar_carpeta(titulo: str = "Seleccionar carpeta") -> str:
    """Abre un diálogo para seleccionar una carpeta."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        root.attributes('-topmost', True)  # Mantener al frente
        
        dname = filedialog.askdirectory(title=titulo)
        
        root.update()
        root.destroy()
        
        return dname or ""
        
    except Exception as e:
        print(f"Error en diálogo de carpeta: {e}")
        return ""


def seleccionar_archivos_multiples(titulo: str = "Seleccionar archivos", 
                                  tipos: Tuple[Tuple[str, str], ...] = (("Todos", "*.*"),)) -> List[str]:
    """Abre un diálogo para seleccionar múltiples archivos."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        root.attributes('-topmost', True)  # Mantener al frente
        
        fnames = filedialog.askopenfilenames(title=titulo, filetypes=tipos)
        
        root.update()
        root.destroy()
        
        return list(fnames) if fnames else []
        
    except Exception as e:
        print(f"Error en diálogo de múltiples archivos: {e}")
        return []
