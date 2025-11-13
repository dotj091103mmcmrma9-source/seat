import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_ventas():
    ventas = tk.Tk() 
    ventas.title("Gestión de Ventas")  
    ventas.geometry("800x500")  # Tamaño compacto

    # Cambiar el color de fondo de la ventana
    ventas.configure(bg="#98cfe9")  # Color de fondo claro

    campos = [
        ("ID Ventas", 0, 0),
        ("Fecha (YYYY-MM-DD)", 1, 0),
        ("ID Sucursal", 2, 0),
        ("N° Clientes", 3, 0),
        ("N° Serie", 4, 0),
        ("Cantidad", 5, 0),
        ("Precio Unitario", 6, 0),
        ("Subtotal", 7, 0),
        ("IVA", 8, 0),
        ("Total", 9, 0)
    ]

    entradas = {}  
    
    for texto, fila, col in campos:
        tk.Label(ventas, text=texto, bg="#b0e0e6").grid(row=fila, column=col, padx=5, pady=5, sticky="w")  # Color de fondo de las etiquetas
        entrada = tk.Entry(ventas, width=20)  # Entradas más compactas
        entrada.grid(row=fila, column=col + 1, padx=5, pady=5, sticky="ew")  # Alinear las entradas
        entradas[texto] = entrada 

    def ejecutar_sql(sql, params=(), fetch=False):
        con = conexion.conectar_bd() 
        cursor = con.cursor()
        cursor.execute(sql, params)  
        if fetch: 
            datos = cursor.fetchall()
            con.close()
            return datos
        else: 
            con.commit()
            con.close()

    def calcular_totales(event=None):
        try:
            cantidad = float(entradas["Cantidad"].get()) 
            precio = float(entradas["Precio Unitario"].get())  
            subtotal = cantidad * precio  
            iva = subtotal * 0.16
            total = subtotal + iva
            entradas["Subtotal"].delete(0, tk.END)
            entradas["Subtotal"].insert(0, f"{subtotal:.2f}")
            entradas["IVA"].delete(0, tk.END)
            entradas["IVA"].insert(0, f"{iva:.2f}")
            entradas["Total"].delete(0, tk.END)
            entradas["Total"].insert(0, f"{total:.2f}")
        except ValueError:
            for campo in ("Subtotal", "IVA", "Total"):
                entradas[campo].delete(0, tk.END)

    entradas["Cantidad"].bind("<KeyRelease>", calcular_totales)
    entradas["Precio Unitario"].bind("<KeyRelease>", calcular_totales)

    def insertar():
        if not entradas["ID Ventas"].get() or not entradas["Fecha (YYYY-MM-DD)"].get() or not entradas["ID Sucursal"].get():
            messagebox.showwarning("Campos vacíos", "ID Ventas, Fecha y Sucursal son obligatorios")
            return
        sql = """INSERT INTO ventas 
        (id_ventas, fecha_venta, id_surcusal, n_clientes, n_serie, cantidad, precio_unitario, subtotal, iva, total) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = tuple(entradas[c].get() for c in [
            "ID Ventas", "Fecha (YYYY-MM-DD)", "ID Sucursal", "N° Clientes", "N° Serie",
            "Cantidad", "Precio Unitario", "Subtotal", "IVA", "Total"
        ])
        ejecutar_sql(sql, params)  
        mostrar_datos() 
        limpiar() 
        messagebox.showinfo("Éxito", "Venta registrada correctamente")

    def actualizar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una venta para actualizar")
            return
        sql = """UPDATE ventas 
        SET fecha_venta=%s, id_surcusal=%s, n_cliente=%s, n_serie=%s, cantidad=%s, precio_unitario=%s, 
        subtotal=%s, iva=%s, total=%s 
        WHERE id_ventas=%s"""
        params = (
            entradas["Fecha (YYYY-MM-DD)"].get(),
            entradas["ID Sucursal"].get(),
            entradas["N° Clientes"].get(),
            entradas["N° Serie"].get(),
            entradas["Cantidad"].get(),
            entradas["Precio Unitario"].get(),
            entradas["Subtotal"].get(),
            entradas["IVA"].get(),
            entradas["Total"].get(),
            entradas["ID Ventas"].get()
        )
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Venta actualizada correctamente")

    def eliminar():
        if not entradas["ID Ventas"].get():
            messagebox.showwarning("Atención", "Seleccione una venta para eliminar")
            return
        ejecutar_sql("DELETE FROM ventas WHERE id_ventas=%s", (entradas["ID Ventas"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Venta eliminada correctamente")

    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)

    def mostrar_datos():
        for row in tabla.get_children(): 
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM ventas", fetch=True) 
        for fila in datos:  
            tabla.insert("", tk.END, values=fila)

    def seleccionar(event):
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            for i, campo in enumerate([
                "ID Ventas", "Fecha (YYYY-MM-DD)", "ID Sucursal", "N° Clientes", "N° Serie", 
                "Cantidad", "Precio Unitario", "Subtotal", "IVA", "Total"
            ]):
                entradas[campo].delete(0, tk.END)
                entradas[campo].insert(0, valores[i])

    # Crear un marco para centrar los botones
    marco_botones = tk.Frame(ventas, bg="#98cfe9")
    marco_botones.grid(row=10, column=0, columnspan=4, pady=10)

    botones = [("Agregar", insertar), ("Actualizar", actualizar), ("Eliminar", eliminar), ("Limpiar", limpiar)]
    for texto, cmd in botones:
        tk.Button(marco_botones, text=texto, width=10, command=cmd, bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

    # Configurar la tabla
    columnas = ("ID Ventas", "Fecha", "ID Sucursal", "N° Clientes", "N° Serie", "Cantidad", "Precio Unitario", "Subtotal", "IVA", "Total")
    tabla = ttk.Treeview(ventas, columns=columnas, show="headings", height=10)
    for col in columnas:
        tabla.heading(col, text=col) 
        tabla.column(col, anchor="center", width=80)  # Alinear al centro
    tabla.grid(row=11, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")  # Centrar la tabla
    tabla.bind("<<TreeviewSelect>>", seleccionar)  

    # Botón para regresar al menú
    tk.Button(ventas, text="Regresar al Menú", width=12,
              command=lambda: [ventas.destroy(), menu.abrir_menu()], bg="#f44336", fg="white", font=("Arial", 10)).grid(row=25, column=0, columnspan=4, pady=10)

    # Configurar la distribución de la cuadrícula para que se expanda
    for i in range(4):
        ventas.grid_columnconfigure(i, weight=1)  # Permitir que las columnas se expandan
    ventas.grid_rowconfigure(10, weight=1)  # Permitir que la fila de botones se expanda
    ventas.grid_rowconfigure(11, weight=1)  # Permitir que la fila de la tabla se expanda

    mostrar_datos()  
    ventas.mainloop()  

if __name__ == "__main__":
    abrir_ventas()