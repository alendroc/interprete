from tkinter import *

#-----------------------------Variables-----------------------------

mainWd = Tk()
mainWd.geometry("700x800")
mainFr = Frame(mainWd)

# Frame del menú que contendrá optionsFr y debuggerFr
menuFr = Frame(mainFr)

optionsFr = Frame(menuFr, bg="gray", height=30)
debuggerFr = Frame(menuFr, bg="white", height=30)

# Frames dinámicos
codeFr = Frame(mainFr, bg="gray")
consoleFr = Frame(mainFr, bg="white")

# Text y Scrollbar
codeTxt = Text(codeFr, wrap='none')  # wrap='none' para no ajustar el texto automáticamente
codeScroll = Scrollbar(codeFr, command=codeTxt.yview)
codeTxt.config(yscrollcommand=codeScroll.set)

#-----------------------------Eventos-----------------------------

def resize(event):
    width = mainFr.winfo_width()
    height = mainFr.winfo_height()

    remaining_height = height - menuFr.winfo_height()

    # Ajustar tamaño y posición de codeFr y consoleFr
    codeFr.place(x=0, y=menuFr.winfo_height(), width=width, height=remaining_height * 0.5)
    consoleFr.place(x=0, y=menuFr.winfo_height() + remaining_height * 0.5, width=width, height=remaining_height * 0.5)

    # Ajustar tamaño de codeTxt y codeScroll dentro de codeFr
    codeFr.grid_propagate(False)  # Evitar que los widgets cambien el tamaño de codeFr
    codeTxt.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
    codeScroll.grid(column=1, row=0, sticky='ns')

    # Ajustar las columnas y filas para que el Text ocupe el espacio disponible
    codeFr.columnconfigure(0, weight=1)  # Permitir que la columna 0 (codeTxt) se expanda
    codeFr.rowconfigure(0, weight=1)

#-----------------------------Frames-----------------------------

mainWd.title("Frame principal")
mainFr.pack(fill=BOTH, expand=True)

# Menu estático
menuFr.pack(fill=X)
optionsFr.pack(fill=X)
debuggerFr.pack(fill=X)  

# Añadir menuFr al mainFr
menuFr.pack_propagate(False)
menuFr.config(height=60)

#-----------------------------Componentes-----------------------------

codeTxt.config(width=300, height=300)
codeTxt.grid(column=0, row=0, padx=10, pady=10)
codeScroll.grid(column=1, row=0)

#-----------------------------Eventos-----------------------------

mainWd.bind('<Configure>', resize)




mainWd.mainloop()