from tkinter import *
from .interprete import *
# from tkinter import ttk, filedialog

class InterpreterView:
    def __init__(self):
        self.mainWd = Tk()
        self.mainWd.geometry("700x800")
        self.mainFr = Frame(self.mainWd)

        # Frame del menú que contendrá optionsFr y debuggerFr
        self.menuFr = Frame(self.mainFr)

        self.optionsFr = Frame(self.menuFr, bg="#dddddd", height=30)
        
        self.optionsFr.pack(fill=X) 
        self.centered_label = Label(self.optionsFr, text="Intérprete Yakuza", bg="#dddddd", font=("Arial", 16), fg="#000000")  
        self.centered_label.pack(expand=True)

        self.debuggerFr = Frame(self.menuFr, bg="white", height=30)

        # Frames dinámicos
        self.codeFr = Frame(self.mainFr, bg="#f0f0f0")
        self.consoleFr = Frame(self.mainFr, bg="#f0f0f0")

        # Text y Scrollbar del código y los números de línea
        self.line_number = Text(self.codeFr, width=4, padx=4, takefocus=0, border=0, background='#DFC57B', state=DISABLED)
        self.codeTxt = Text(self.codeFr, wrap='none')  
        self.scrollbar = Scrollbar(self.codeFr, command=self.on_scroll)
        self.codeTxt.config(yscrollcommand=self.scrollbar.set)
        self.line_number.config(yscrollcommand=self.scrollbar.set)

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

        # Actualizar las líneas de número
        self.codeTxt.bind("<KeyRelease>", self.update_line_numbers)
        self.codeTxt.bind("<MouseWheel>", self.sync_scroll)

        # Ejecución
        self.mainWd.bind('<Configure>', self.resize)
        self.mainWd.mainloop()

    def update_line_numbers(self, event=None):
        line_numbers_content = "\n".join(str(i) for i in range(1, int(self.codeTxt.index('end').split('.')[0])))
        self.line_number.config(state=NORMAL)
        self.line_number.delete(1.0, END)
        self.line_number.insert(1.0, line_numbers_content)
        self.line_number.config(state=DISABLED)

    def on_scroll(self, *args):
        self.codeTxt.yview(*args)
        self.line_number.yview(*args)

    def sync_scroll(self, event=None):
        self.codeTxt.yview_scroll(-1 * int(event.delta / 120), "units")
        self.line_number.yview_scroll(-1 * int(event.delta / 120), "units")
        return "break"


    def onEjecEvent(self):
        try:
            self.consoleTxt.config(state=NORMAL)
            codigoEntrada = self.codeTxt.get("1.0", END)
            self.consoleTxt.delete(1.0, END)
            self.consoleTxt.insert(1.0, ejecutar(codigoEntrada))
            self.consoleTxt.config(state=DISABLED)

        except TclError:
            pass


    def onCompileEvent(self):
        try:
            self.consoleTxt.config(state=NORMAL)
            codigoEntrada = self.codeTxt.get("1.0", END)
            self.consoleTxt.delete(1.0, END)
            mensaje,analisisSintac=compilar(codigoEntrada)
            self.consoleTxt.insert(1.0, mensaje)
            self.consoleTxt.config(state=DISABLED)
        except TclError:
            pass

    def setup_ui(self):
        self.mainWd.title("Interpretador Yakuza")
        self.mainFr.pack(fill=BOTH, expand=True)

        # Menu estático
        self.menuFr.pack(fill=X)
        self.optionsFr.pack(fill=X)
        self.debuggerFr.pack(fill=X)  

        # Crear el navbar
        self.create_navbar()

        # Añadir componentes
        self.line_number.grid(column=0, row=0, padx=10, pady=10, sticky='ns')
        self.codeTxt.grid(column=1, row=0, padx=10, pady=10, sticky='nsew')
        self.scrollbar.grid(column=2, row=0, sticky='ns')

        self.consoleTxt.grid(column=0, row=0, padx=10, pady=10)
        self.consoleScroll.grid(column=1, row=0)

        # Botones
        self.ejecBtn.pack(side=RIGHT, anchor="e", padx=[5, 5])
        self.compBtn.pack(side=RIGHT, anchor="e", padx=[5, 5])

    #AQUI INICIA EL NAVBAR
    def create_navbar(self):
        # Crear barra de menú
        self.menu_bar = Menu(self.mainWd)
        
        # Crear menú Opciones, Nosostros y Vista
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.vista_menu = Menu(self.menu_bar, tearoff=0)
        self.nosotros_menu = Menu(self.menu_bar, tearoff=0)
        # Poner todas las opciones que tendrá
        self.options_menu.add_command(label="Guardar")
        self.options_menu.add_command(label="Guardar como...")
        self.vista_menu.add_command(label="Cambiar Tema", command=self.cambiarTema)
       
        # Añadir el menú "Opciones" a la barra de menú
        self.menu_bar.add_cascade(label="Opciones", menu=self.options_menu)
        self.menu_bar.add_cascade(label="Vista", menu=self.vista_menu)
        self.menu_bar.add_cascade(label="Sobre Nosotros")
        # Configurar la barra de menú en la ventana principal
        self.mainWd.config(menu=self.menu_bar)

    def cambiarTema(self):
        # Simplemente va cambiar al contrario
        current_bg = self.codeFr.cget("bg")
        if current_bg == "#f0f0f0":
            self.line_number.config(bg="#CC6CE7")
            self.codeFr.config(bg="#2e2e2e")
            self.consoleFr.config(bg="#2e2e2e")
            self.codeTxt.config(bg="#1e1e1e", fg="white")
            self.consoleTxt.config(bg="#1e1e1e", fg="white")
        else:
            self.line_number.config(bg="#E6DCE8")
            self.codeFr.config(bg="#f0f0f0")
            self.consoleFr.config(bg="#f0f0f0")
            self.codeTxt.config(bg="white",fg="black")
            self.consoleTxt.config(bg="white", fg="black")

    
    #Funciones de guardar 
    #def guardar(self):
        
    
    #def guardarComo(self):
      

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

        self.codeFr.columnconfigure(1, weight=1)  # Ajuste para que el área de texto sea responsive
        self.consoleFr.columnconfigure(0, weight=1)  
        self.consoleFr.rowconfigure(0, weight=1)
