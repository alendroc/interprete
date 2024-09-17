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

codeTxt = Text(codeFr)

#-----------------------------Eventos-----------------------------

def resize(event):
    width = mainFr.winfo_width()
    height = mainFr.winfo_height()

    remaining_height = height - menuFr.winfo_height()

    codeFr.place(x=0, y=menuFr.winfo_height(), width=width, height=remaining_height * 0.5)
    consoleFr.place(x=0, y=menuFr.winfo_height() + remaining_height * 0.5, width=width, height=remaining_height * 0.5)

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

codeTxt.grid(column=0, row=0, padx=10, pady=10)

#-----------------------------Eventos-----------------------------

mainWd.bind('<Configure>', resize)




mainWd.mainloop()