import tkinter as tk
from tkinter import messagebox 
import menu 
usuario_correcto = "jorge"
pass_correcto = "12345678"

def mostrar_login():
    ventana_login = tk.Tk()
    ventana_login.title("Login") 
    ventana_login.geometry("500x400")
    
    def verificar_login():       
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()
        
        if not usuario or not contraseña:
            messagebox.showwarning("Campos vacios", "Por favor, ingrese usuario y contraseña.")
            return
        if usuario == usuario_correcto and contraseña == pass_correcto:
            messagebox.showinfo("Dtos correcto", f"¡Bienvenida, {usuario}!")
            ventana_login.destroy() 
            menu.abrir_menu()
        else:
            messagebox.showerror("Error", "Usuarioo contraseña incorrectos.")
    tk.Label(ventana_login, text="Usuario:").pack(pady=5)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()
    entry_usuario.focus()
    
    tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
    entry_contraseña = tk.Entry(ventana_login, show="*") 
    entry_contraseña.pack()
    
    tk.Button(ventana_login, text="Iniciar sesion", command=verificar_login).pack(pady=21)
    tk.Button(ventana_login, text="Salir", command=ventana_login.destroy).pack(pady=20)
    
    ventana_login.mainloop()
    
if __name__ == "__main__":
    mostrar_login()