def seleccionar_archivo(titulo="Seleccionar archivo", tipos=(("Todos","*.*"),)):
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk(); root.withdraw()
    fname = filedialog.askopenfilename(title=titulo, filetypes=tipos)
    root.update(); root.destroy()
    return fname or ""

def seleccionar_carpeta(titulo="Seleccionar carpeta"):
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk(); root.withdraw()
    dname = filedialog.askdirectory(title=titulo)
    root.update(); root.destroy()
    return dname or ""
