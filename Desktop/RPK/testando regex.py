import tkinter as tk
import re

class Tooltip:
    """Classe para criar um tooltip"""
    def __init__(self, widget):
        self.widget = widget
        self.tooltip_window = None

    def show_tooltip(self, message):
        if self.tooltip_window is not None:
            return
        
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=message, bg="lightyellow", relief="solid", borderwidth=1)
        label.pack()
        
    def hide_tooltip(self):
        if self.tooltip_window is not None:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def validar_entry():
    texto = entry.get()
    regex = r'^Set Acc ([1-9][0-9]?) Dec ([1-9][0-9]?)$'
    
    if re.match(regex, texto):
        tooltip.show_tooltip("Válido!")
    else:
        tooltip.show_tooltip("Inválido! Exemplo válido: 35/20")

    # Esconde o tooltip após alguns segundos
    root.after(2000, tooltip.hide_tooltip)

# Cria a janela principal
root = tk.Tk()
root.title("Validação de Entry com Tooltip")

# Cria a Entry
entry = tk.Entry(root)
entry.pack(pady=10)

# Cria o botão que irá validar a entrada
validar_botao = tk.Button(root, text="Validar", command=validar_entry)
validar_botao.pack(pady=5)

# Cria a tooltip para o botão
tooltip = Tooltip(validar_botao)

# Inicia o loop principal
root.mainloop()
