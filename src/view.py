from tkinter import *

#-----------------------------Eventos-----------------------------

def onEjecEvent():
    print("Hola")


def onCompileEvent():
    consoleTxt.config(state=NORMAL)
    consoleTxt.insert(1.0, "Hola Mundo")
    consoleTxt.config(state=DISABLED)


#-----------------------------Variables-----------------------------

mainWd = Tk()
mainWd.geometry("700x800")
mainFr = Frame(mainWd)

# Frame del menú que contendrá optionsFr y debuggerFr
menuFr = Frame(mainFr)

optionsFr = Frame(menuFr, bg="#dddddd", height=30)
debuggerFr = Frame(menuFr, bg="white", height=30)

# Frames dinámicos
codeFr = Frame(mainFr, bg="#f0f0f0")
consoleFr = Frame(mainFr, bg="#f0f0f0")

# Text y Scrollbar del código
codeTxt = Text(codeFr, wrap='none')  # wrap='none' para no ajustar el texto automáticamente
codeScroll = Scrollbar(codeFr, command=codeTxt.yview)
codeTxt.config(yscrollcommand=codeScroll.set)

# Text y Scrollbar de la consolo
consoleTxt = Text(consoleFr, wrap='none')  # wrap='none' para no ajustar el texto automáticamente
consoleScroll = Scrollbar(consoleFr, command=consoleTxt.yview)
consoleTxt.config(yscrollcommand=consoleScroll.set, state=DISABLED)

# Separador simulado entre codeFr y consoleFr
separatorFr = Frame(mainFr, bg="#b0b0b0", height=2)

# Botones Run y Stop

ejecBtn = Button(debuggerFr, text="Ejecutar", command=onEjecEvent)
compBtn = Button(debuggerFr, text="Compilar", command=onCompileEvent)

#-----------------------------Posicionamiento-----------------------------

def resize(event):
    width = mainFr.winfo_width()
    height = mainFr.winfo_height()

    remaining_height = height - menuFr.winfo_height()

    # Ajustar tamaño y posición de codeFr y consoleFr y un separador entre ellos
    codeFr.place(x=0, y=menuFr.winfo_height(), width=width, height=remaining_height * 0.5)
    separatorFr.place(x=0, y=menuFr.winfo_height() + remaining_height * 0.5, width=width, height=2)
    consoleFr.place(x=0, y=menuFr.winfo_height() + remaining_height * 0.5, width=width, height=remaining_height * 0.5)

    # Ajustar tamaño de codeTxt y codeScroll dentro de codeFr
    codeFr.grid_propagate(False)  # Evitar que los widgets cambien el tamaño de codeFr
    codeTxt.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
    codeScroll.grid(column=1, row=0, sticky='ns')
    
    # Ajustar tamaño de codeTxt y codeScroll dentro de codeFr
    consoleFr.grid_propagate(False)  # Evitar que los widgets cambien el tamaño de codeFr
    consoleTxt.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
    consoleScroll.grid(column=1, row=0, sticky='ns')

    # Ajustar las columnas y filas para que el Text ocupe el espacio disponible
    codeFr.columnconfigure(0, weight=1)  # Permitir que la columna 0 (codeTxt) se expanda
    codeFr.rowconfigure(0, weight=1)
    
    consoleFr.columnconfigure(0, weight=1)  # Permitir que la columna 0 (codeTxt) se expanda
    consoleFr.rowconfigure(0, weight=1)
    
    # Ajustar los botones hacia la derecha del menu
    
    ejecBtn.pack(side=RIGHT, anchor="e", padx=[5, 5])
    compBtn.pack(side=RIGHT, anchor="e", padx=[5, 5])

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

# Añadir bordes a los frames

#codeFr.config(relief=RAISED, bd=3)

#-----------------------------Componentes-----------------------------

codeTxt.config(width=300, height=300)
codeTxt.grid(column=0, row=0, padx=10, pady=10)
codeScroll.grid(column=1, row=0)

#-----------------------------Ejecución-----------------------------

mainWd.bind('<Configure>', resize)

mainWd.mainloop()