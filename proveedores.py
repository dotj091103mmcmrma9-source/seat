import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_proveedores():
    proveedores = tk.Tk()
    proveedores.title("Gestión de Proveedores")
    proveedores.geometry("700x600")
    proveedores.configure(bg="#B3FCA9")  # Color de fondo

    
    font_label = ("Arial", 12)
    font_entry = ("Arial", 12)
    font_button = ("Arial", 10, "bold")


    frame = tk.Frame(proveedores, bg="#B3FCA9")
    frame.pack(expand=True)

  
    title_label = tk.Label(frame, font=("Arial", 16, "bold"), bg="#B3FCA9", fg="#4CAF50")
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    campos = ["RFC", "n_proveedores", "domicilio", "telefono"] 
    entradas = {}

    for i, texto in enumerate(campos):
        tk.Label(frame, text=texto, font=font_label, bg="#EE8B7E", fg="#070606").grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
        entradas[texto] = tk.Entry(frame, font=font_entry)
        entradas[texto].grid(row=i+1, column=1, padx=10, pady=5)
        entradas[texto].configure(bg="#FFFFFF", fg="#000000")  
    def ejecutar_sql(sql, params=(), fetch=False):
        con = conexion.conectar_bd()
        cursor = con.cursor()
        cursor.execute(sql, params)
        if fetch:
            resultado = cursor.fetchall()
            con.close()
            return resultado
        else:
            con.commit()
            con.close()
             
    def insertar():
        if any(not entradas[c].get() for c in campos):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
            return
        sql = "INSERT INTO proveedores (RFC, n_proveedores, domicilio, telefono) VALUES (%s, %s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
        
    def actualizar(): 
        if not entradas["telefono"].get():
            messagebox.showwarning("Atención", "Seleccione un dato para actualizar")
            return
        sql = "UPDATE proveedores SET RFC=%s, n_proveedores=%s, domicilio=%s WHERE telefono=%s"
        params = (entradas["RFC"].get(), entradas["n_proveedores"].get(),
                  entradas["domicilio"].get(), entradas["telefono"].get())
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Dato actualizado correctamente")
        
    def eliminar():
        if not entradas["telefono"].get():
            messagebox.showwarning("Atención", "Seleccione un dato para eliminar")
            return
        sql = "DELETE FROM proveedores WHERE telefono=%s"
        ejecutar_sql(sql, (entradas["telefono"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Dato eliminado correctamente")
        
    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)
            
    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM proveedores", fetch=True)
        for fila in datos:
            tabla.insert("", tk.END, values=fila)

    def seleccionar(event):
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            for i, c in enumerate(campos):
                entradas[c].delete(0, tk.END)
                entradas[c].insert(0, valores[i])

    botones = [("Agregar", insertar), ("Actualizar", actualizar), ("Eliminar", eliminar), ("Limpiar", limpiar)]
    for i, (texto, cmd) in enumerate(botones):
        tk.Button(frame, text=texto, width=12, command=cmd, font=font_button, bg="#4CAF50", fg="#FFFFFF").grid(row=5, column=i, padx=10, pady=10)

    columnas = ("RFC", "n_proveedores", "domicilio", "telefono")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.grid(row=6, column=0, columnspan=4, padx=10, pady=20)
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    tk.Button(frame, text="Regresar al Menú", width=20,
              command=lambda: [proveedores.destroy(), menu.abrir_menu()], bg="#F0EDD9", fg="#0C0A0A").grid(row=7, column=0, columnspan=4, pady=10)

    mostrar_datos()
    proveedores.mainloop()

if __name__ == "__main__":
    abrir_proveedores()