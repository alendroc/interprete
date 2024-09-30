from tkinter import *
from .interprete import *
from tkinter import ttk, filedialog
import webbrowser
from tkinter import Toplevel, Label, Button, PhotoImage

class InterpreterView:
    def __init__(self):
        # Variable para almacenar la ruta del archivo actual
        self.current_file = None
        
        self.tittle = "Interpretador Yakuza"
        
        self.mainWd = Tk()
        self.mainWd.geometry("700x800")
        self.mainFr = Frame(self.mainWd)
        # Llamar a la creación de estilos
        self.create_button_style()

        # Frame del menú que contendrá optionsFr y debuggerFr
        self.menuFr = Frame(self.mainFr)

        self.optionsFr = Frame(self.menuFr, bg="#dddddd", height=30)
        
        self.optionsFr.pack(fill=X) 
        self.centered_label = Label(self.optionsFr, text="Intérprete Yakuza", bg="#dddddd", font=("Consolas", 13), fg="#000000")  
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

      # Botones Ejecutar y Compilar con el estilo creado
        self.ejecBtn = ttk.Button(self.debuggerFr, text="Ejecutar", style="Custom.TButton", command=self.onEjecEvent)
        self.compBtn = ttk.Button(self.debuggerFr, text="Compilar", style="Custom.TButton", command=self.onCompileEvent)

        # Posicionamiento
        self.setup_ui()

        # Actualizar las líneas de número
        self.codeTxt.bind("<KeyRelease>", self.update_line_numbers)
        self.codeTxt.bind("<MouseWheel>", self.sync_scroll)

        # Ejecución
        self.mainWd.bind('<Configure>', self.resize)
        self.mainWd.mainloop()


    def create_button_style(self):
        style = ttk.Style()
        
        # Estilo para el botón personalizado
        style.configure("Custom.TButton", 
                        font=("Consolas", 10, "bold"),       # Fuente y tamaño de texto
                        padding=5,                          # Espacio interno
                        foreground="#242424",               # Color del texto
                        background="#f0f0f0",               # Color de fondo
                        borderwidth=0,                      # Sin borde del botón
                        relief="solid",                      # Relieve plano
                        focuscolor="none")                  # Sin color de enfoque

        # Ajustar el color al pasar el ratón (hover)
        style.map("Custom.TButton", 
                foreground=[("active", "#8D6F64")],      # Color del texto al pasar el ratón
                background=[("active", "#8D6F64")])      # Color de fondo al pasar el ratón


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
        self.mainWd.title(self.tittle)
        self.mainFr.pack(fill=BOTH, expand=True)

        # Menu estático
        self.menuFr.pack(fill=X)
        self.optionsFr.pack(fill=X)
        self.debuggerFr.pack(fill=X)  

        # Crear el navbar directamente aquí
        self.menu_bar = Menu(self.mainWd)
        
        # Crear menú Opciones, Nosotros y Vista
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.vista_menu = Menu(self.menu_bar, tearoff=0)
        self.nosotros_menu = Menu(self.menu_bar, tearoff=0)

        # Poner todas las opciones que tendrá
        self.options_menu.add_command(label="Nuevo archivo", command=self.nuevo_archivo)
        self.options_menu.add_command(label="Abrir archivo", command=self.abrir_archivo)
        self.options_menu.add_command(label="Guardar", command=self.guardar)
        self.options_menu.add_command(label="Guardar como...", command=self.guardar_como)
        self.vista_menu.add_command(label="Cambiar Tema", command=self.cambiarTema)
        
        self.nosotros_menu.add_command(label="Preguntas Frecuentes", command=self.abrir_faq)
        self.nosotros_menu.add_command(label="Contáctanos", command=self.contactanos)

        # Añadir el menú "Opciones", "Vista" y "Sobre Nosotros" a la barra de menú
        self.menu_bar.add_cascade(label="Opciones", menu=self.options_menu)
        self.menu_bar.add_cascade(label="Vista", menu=self.vista_menu)
        self.menu_bar.add_cascade(label="Sobre Nosotros", menu=self.nosotros_menu)

        # Configurar la barra de menú en la ventana principal
        self.mainWd.config(menu=self.menu_bar)

        # Añadir componentes
        self.line_number.grid(column=0, row=0, padx=10, pady=10, sticky='ns')
        self.codeTxt.grid(column=1, row=0, padx=10, pady=10, sticky='nsew')
        self.scrollbar.grid(column=2, row=0, sticky='ns')

        # Configurar la consola con scrollbar
        self.consoleTxt.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        self.consoleScroll.grid(column=1, row=0, sticky='ns')

        # Cambiar el tamaño de la consola
        self.consoleFr.columnconfigure(0, weight=1)
        self.consoleFr.rowconfigure(0, weight=1)


        # Botones
        self.ejecBtn.pack(side=RIGHT, anchor="e", padx=[5, 5])
        self.compBtn.pack(side=RIGHT, anchor="e", padx=[5, 5])

    
    def abrir_faq(self):
        # Abrir enlace en el navegador
        webbrowser.open("https://docs.google.com/document/d/1spJ9EGqIvaEnNoeNo78z1VbtRsr9yTuUOGOgNib3Agw/edit")  # Cambia por el enlace real

    def contactanos(self):
        contact_window = Toplevel(self.mainWd)
        contact_window.title("Contáctanos")
        contact_window.geometry("600x400")

        # Evitar que se pueda redimensionar la ventana
        contact_window.resizable(False, False)

        # Crear el frame para contener los contactos
        contacts_frame = Frame(contact_window)
        contacts_frame.pack(pady=20)

        # Lista de contactos con su nombre, correo, GitHub y LinkedIn
        contactos = [
            {"nombre": "Daniel González", "correo": "daniel.gonzalez.picado@est.una.ac.cr", "github": "https://github.com/DanielVanetti", "linkedin": "https://www.linkedin.com/in/daniel-gonz%C3%A1lez-picado-519685283/"},
            {"nombre": "Josué Solórzano", "correo": "josue.solorzano.ordoñez@est.una.ac.cr", "github": "https://github.com/JosueCR170", "linkedin": "https://www.linkedin.com/in/persona2/"},
            {"nombre": "Alejandro Chaves", "correo": "jose.chaves.ramirez@est.una.ac.cr", "github": "https://github.com/alendroc", "linkedin": "https://www.linkedin.com/in/jose-alejandro-chaves-ramirez-497839188/"},
            {"nombre": "Randy Villarreal", "correo": "randy.villarreal.fallas@est.una.ac.cr", "github": "https://github.com/Pipe1844", "linkedin": "https://www.linkedin.com/in/persona4/"},
        ]

        for contact in contactos:
            # Crear un frame para cada contacto
            contact_frame = Frame(contacts_frame)
            contact_frame.pack(pady=10, fill="x")  # Aumentar el espacio entre contactos

            # Mostrar el nombre de la persona
            nombre_label = Label(contact_frame, text=contact["nombre"], font=("Consolas", 12, "bold"))
            nombre_label.pack()

            # Mostrar el correo de la persona
            correo_label = Label(contact_frame, text=contact["correo"], font=("Consolas", 10))
            correo_label.pack()

            # Crear botones de GitHub y LinkedIn como texto hipervínculo
            github_button = Button(contact_frame, text="GitHub", command=lambda url=contact["github"]: self.open_link(url), relief=FLAT, fg="blue", cursor="hand2")
            github_button.pack(side=LEFT, padx=5)

            linkedin_button = Button(contact_frame, text="LinkedIn", command=lambda url=contact["linkedin"]: self.open_link(url), relief=FLAT, fg="blue", cursor="hand2")
            linkedin_button.pack(side=LEFT, padx=5)

        # Botón para cerrar la ventana
        close_btn = Button(contact_window, text="Cerrar", command=contact_window.destroy)
        close_btn.pack(pady=20)

    def open_link(self, url):
        webbrowser.open(url)


    def cambiarTema(self):
        # Simplemente va cambiar al contrario
        current_bg = self.codeFr.cget("bg")
        if current_bg == "#f0f0f0":
            # Cambiar a tema oscuro
            self.codeFr.config(bg="#2e2e2e")
            self.consoleFr.config(bg="#2e2e2e")
            self.codeTxt.config(bg="#1e1e1e", fg="white", insertbackground="white")  # Cambiar cursor a blanco
            self.consoleTxt.config(bg="#1e1e1e", fg="white", insertbackground="white")  # Cambiar cursor a blanco
        else:
            # Cambiar a tema claro
            self.codeFr.config(bg="#f0f0f0")
            self.consoleFr.config(bg="#f0f0f0")
            self.codeTxt.config(bg="white", fg="black", insertbackground="black")  # Cambiar cursor a negro
            self.consoleTxt.config(bg="white", fg="black", insertbackground="black")  # Cambiar cursor a negro


    def nuevo_archivo(self):
        self.current_file = None
        self.codeTxt.delete("1.0", END)
        self.update_line_numbers()
        self.mainWd.title(self.tittle)

    def abrir_archivo(self):
        file_path = filedialog.askopenfilename(
        title="Abrir archivo", 
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            
            with open(self.current_file, 'r') as file:
                text = file.read()
                self.codeTxt.delete("1.0", END)
                self.codeTxt.insert("1.0", text)
                self.update_line_numbers()
                self.mainWd.title(file_path)
        else:
            self.guardar_como()   

    def guardar(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.codeTxt.get("1.0", END))
        else:
            self.guardar_como()

    def guardar_como(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            with open(self.current_file, 'w') as file:
                file.write(self.codeTxt.get("1.0", END))
                self.mainWd.title(file_path)
                
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

    