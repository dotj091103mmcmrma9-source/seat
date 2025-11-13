import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_sucursal():
    sucursal = tk.Tk()
    sucursal.title("Gestión de sucursal")
    sucursal.geometry("700x600")
    
    # Cambiar el color de fondo de la ventana
    sucursal.configure(bg="#9bd5dd")  # Color azul claro

    campos = ["id_sucursal", "telefono", "domicilio", "n_sucursal"] 
    entradas = {}
    
    for i, texto in enumerate(campos):
        tk.Label(sucursal, text=texto, bg="#bfc9c9").grid(row=i, column=0, padx=10, pady=5, sticky="e")  # Alinear etiquetas a la derecha
        entradas[texto] = tk.Entry(sucursal)
        entradas[texto].grid(row=i, column=1, padx=10, pady=5, sticky="w")  # Alinear entradas a la izquierda
        
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
        sql = "INSERT INTO sucursal (id_sucursal, telefono, domicilio, n_sucursal) VALUES (%s, %s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Sucursal agregado correctamente")
        
    def actualizar(): 
        if not entradas["codigo"].get():
            messagebox.showwarning("Atención", "Seleccione un dato para actualizar")
            return
        sql = "UPDATE sucursal SET id_sucursal=%s,telefono=%s, domicilio=%s WHERE n_sucursal=%s"
        params = (entradas["id_sucursal"].get(), entradas["telefono"].get(),
                  entradas["domicilio"].get(), entradas["n_sucursal"].get())
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Dato actualizado correctamente")
        
    def eliminar():
        if not entradas["codigo"].get():
            messagebox.showwarning("Atención", "Seleccione un dato para eliminar")
            return
        sql = "DELETE FROM sucursal WHERE codigo=%s"
        ejecutar_sql(sql, (entradas["codigo"].get(),))
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
        tk.Button(sucursal, text=texto, width=12, command=cmd, bg="#4CAF50", fg="white").grid(row=4, column=i, padx=10, pady=10)

    columnas = ("id_sucursal", "telefono", "domicilio", "n_sucursal")
    tabla = ttk.Treeview(sucursal, columns=columnas, show="headings", height=12)
    
    # Configurar la alineación de las columnas al centro
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)  # Alinear al centro

    tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=20)
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    tk.Button(sucursal, text="Regresar al Menú", width=20,
              command=lambda: [sucursal.destroy(), menu.abrir_menu()], bg="#f44336", fg="white").grid(row=7, column=0, columnspan=4, pady=10)

    mostrar_datos()
    sucursal.mainloop()

if __name__ == "__main__":
    abrir_sucursal()