import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_clientes():
    clientes = tk.Tk()
    clientes.title("Gestión de Clientes")
    clientes.geometry("700x600")
    clientes.configure(bg="#A0D4EC")  # Color de fondo

    # Crear un marco para centrar el contenido
    frame = tk.Frame(clientes, bg="#A0D4EC")
    frame.pack(expand=True, padx=20, pady=20)

    campos = ["RFC", "nom_cliente", "edad", "domicilio", "telefono"] 
    entradas = {}
    
    for i, texto in enumerate(campos):
        tk.Label(frame, text=texto, bg="#A7EEB9", fg="#000000", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entradas[texto] = tk.Entry(frame, font=("Arial", 12))
        entradas[texto].grid(row=i, column=1, padx=10, pady=5)
        entradas[texto].configure(bg="#FFFFFF", fg="#000000")  # Color de fondo y texto de las entradas
        
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
        sql = "INSERT INTO clientes (RFC, nom_cliente, edad, domicilio, telefono) VALUES (%s, %s, %s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Cliente agregado correctamente")
        
    def actualizar(): 
        if not entradas["RFC"].get():
            messagebox.showwarning("Atención", "Seleccione un cliente para actualizar")
            return
        sql = "UPDATE clientes SET nom_cliente=%s, edad=%s, domicilio=%s, telefono=%s WHERE RFC=%s"
        params = (entradas["nom_cliente"].get(), entradas["edad"].get(),
                  entradas["domicilio"].get(), entradas["telefono"].get(), entradas["RFC"].get())
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        
    def eliminar():
        if not entradas["RFC"].get():
            messagebox.showwarning("Atención", "Seleccione un cliente para eliminar")
            return
        sql = "DELETE FROM clientes WHERE RFC=%s"
        ejecutar_sql(sql, (entradas["RFC"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
        
    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)
            
    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM clientes", fetch=True)
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
        tk.Button(frame, text=texto, width=12, command=cmd, bg="#4CAF50", fg="#FFFFFF", font=("Arial", 12)).grid(row=5, column=i, padx=10, pady=10)

    columnas = ("RFC", "nom_cliente", "edad", "domicilio", "telefono")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.grid(row=6, column=0, columnspan=4, padx=10, pady=20)
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    tk.Button(frame, text="Regresar al Menú", width=20,
              command=lambda: [clientes.destroy(), menu.abrir_menu()], bg="#F44336", fg="#FFFFFF", font=("Arial", 12)).grid(row=7, column=0, columnspan=4, pady=10)

    mostrar_datos()
    clientes.mainloop()

if __name__ == "__main__":
    abrir_clientes()