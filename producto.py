import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_producto():
    producto = tk.Tk()
    producto.title("Gestión de Producto")
    producto.geometry("600x700")  # Ajustar el tamaño de la ventana
    producto.configure(bg="#98DAF8")  

    campos = ["n_serie", "marca", "nombre_pro", "modelo", "RFC"] 
    entradas = {}
    
    # Crear un marco para los campos de entrada
    frame_campos = tk.Frame(producto, bg="#98DAF8")
    frame_campos.pack(pady=20)

    for i, texto in enumerate(campos):
        tk.Label(frame_campos, text=texto, bg="#77A2E2", fg="#0E0B0B").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entradas[texto] = tk.Entry(frame_campos)
        entradas[texto].grid(row=i, column=1, padx=10, pady=5, sticky="w")
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
        sql = "INSERT INTO producto (n_serie, marca, nombre_pro, modelo, RFC) VALUES (%s, %s, %s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Producto agregado correctamente")
        
    def actualizar(): 
        if not entradas["n_serie"].get():
            messagebox.showwarning("Atención", "Seleccione un producto para actualizar")
            return
        sql = "UPDATE producto SET marca=%s, nombre_pro=%s, modelo=%s, RFC=%s WHERE n_serie=%s"
        params = (entradas["marca"].get(), entradas["nombre_pro"].get(),
                  entradas["modelo"].get(), entradas["RFC"].get(), entradas["n_serie"].get())
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Producto actualizado correctamente")
        
    def eliminar():
        if not entradas["n_serie"].get():
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar")
            return
        sql = "DELETE FROM producto WHERE n_serie=%s"
        ejecutar_sql(sql, (entradas["n_serie"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        
    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)
            
    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM producto", fetch=True)
        for fila in datos:
            tabla.insert("", tk.END, values=fila)

    def seleccionar(event):
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            for i, c in enumerate(campos):
                entradas[c].delete(0, tk.END)
                entradas[c].insert(0, valores[i])

    # Crear un marco para los botones
    frame_botones = tk.Frame(producto, bg="#98DAF8")
    frame_botones.pack(pady=20)

    botones = [("Agregar", insertar), ("Actualizar", actualizar), ("Eliminar", eliminar), ("Limpiar", limpiar)]
    for i, (texto, cmd) in enumerate(botones):
        tk.Button(frame_botones, text=texto, width=12, command=cmd, bg="#4CAF50", fg="#FFFFFF").pack(side=tk.LEFT, padx=10)

    # Crear un marco para la tabla
    frame_tabla = tk.Frame(producto, bg="#98DAF8")
    frame_tabla.pack(pady=20)

    columnas = ("n_serie", "marca", "nombre_pro", "modelo", "RFC")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)  # Ajustar el ancho para que se vea mejor
    tabla.pack(padx=10, pady=10)

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    tk.Button(producto, text="Regresar al menú", width=20,
              command=lambda: [producto.destroy(), menu.abrir_menu()], bg="#F44336", fg="#FFFFFF").pack(pady=10)  # Centrar botón de regreso

    mostrar_datos()
    producto.mainloop()

if __name__ == "__main__":
    abrir_producto()