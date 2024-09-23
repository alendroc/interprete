from tkinter import *
from .interprete import compilar

class InterpreterView:
    def __init__(self):
        self.mainWd = Tk()
        self.mainWd.geometry("700x800")
        self.mainFr = Frame(self.mainWd)

        # Frame del menú que contendrá optionsFr y debuggerFr
        self.menuFr = Frame(self.mainFr)

        self.optionsFr = Frame(self.menuFr, bg="#dddddd", height=30)
        self.debuggerFr = Frame(self.menuFr, bg="white", height=30)

        # Frames dinámicos
        self.codeFr = Frame(self.mainFr, bg="#f0f0f0")
        self.consoleFr = Frame(self.mainFr, bg="#f0f0f0")

        # Text y Scrollbar del código
        self.codeTxt = Text(self.codeFr, wrap='none')  
        self.codeScroll = Scrollbar(self.codeFr, command=self.codeTxt.yview)
        self.codeTxt.config(yscrollcommand=self.codeScroll.set)

        # Text y Scrollbar de la consola
        self.consoleTxt = Text(self.consoleFr, wrap='none')  
        self.consoleScroll = Scrollbar(self.consoleFr, command=self.consoleTxt.yview)
        self.consoleTxt.config(yscrollcommand=self.consoleScroll.set, state=DISABLED)

        # Separador simulado entre codeFr y consoleFr
        self.separatorFr = Frame(self.mainFr, bg="#b0b0b0", height=2)

        # Botones Run y Stop
        self.ejecBtn = Button(self.debuggerFr, text="Ejecutar", command=self.onEjecEvent)
        self.compBtn = Button(self.debuggerFr, text="Compilar", command=self.onCompileEvent)

        # Posicionamiento
        self.setup_ui()

        # Ejecución
        self.mainWd.bind('<Configure>', self.resize)
        self.mainWd.mainloop()

    def onEjecEvent(self):
        print("Hola")

    def onCompileEvent(self):
        try:
            self.consoleTxt.config(state=NORMAL)
            codigoEntrada=self.codeTxt.get("1.0", END)
            self.consoleTxt.delete(1.0,END)
            self.consoleTxt.insert(1.0, compilar(codigoEntrada))
            self.consoleTxt.config(state=DISABLED)
        except TclError:
       
            pass

    def setup_ui(self):
        self.mainWd.title("Frame principal")
        self.mainFr.pack(fill=BOTH, expand=True)

        # Menu estático
        self.menuFr.pack(fill=X)
        self.optionsFr.pack(fill=X)
        self.debuggerFr.pack(fill=X)  

        # Añadir menuFr al mainFr
        self.menuFr.pack_propagate(False)
        self.menuFr.config(height=60)

        # Añadir componentes
        self.codeTxt.grid(column=0, row=0, padx=10, pady=10)
        self.codeScroll.grid(column=1, row=0)

        self.consoleTxt.grid(column=0, row=0, padx=10, pady=10)
        self.consoleScroll.grid(column=1, row=0)

        # Botones
        self.ejecBtn.pack(side=RIGHT, anchor="e", padx=[5, 5])
        self.compBtn.pack(side=RIGHT, anchor="e", padx=[5, 5])

    def resize(self, event):
        width = self.mainFr.winfo_width()
        height = self.mainFr.winfo_height()

        remaining_height = height - self.menuFr.winfo_height()

        self.codeFr.place(x=0, y=self.menuFr.winfo_height(), width=width, height=remaining_height * 0.5)
        self.separatorFr.place(x=0, y=self.menuFr.winfo_height() + remaining_height * 0.5, width=width, height=2)
        self.consoleFr.place(x=0, y=self.menuFr.winfo_height() + remaining_height * 0.5, width=width, height=remaining_height * 0.5)

        # Ajustar tamaños
        self.codeFr.grid_propagate(False)  
        self.consoleFr.grid_propagate(False)  

        self.codeFr.columnconfigure(0, weight=1)  
        self.codeFr.rowconfigure(0, weight=1)
        self.consoleFr.columnconfigure(0, weight=1)  
        self.consoleFr.rowconfigure(0, weight=1)